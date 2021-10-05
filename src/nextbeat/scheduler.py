import asyncio
import dataclasses
import threading
import traceback
from asyncio import Task
from typing import (
    Dict,
    List,
    Tuple,
    Iterable,
    Optional,
    Callable,
    Awaitable,
    Sequence,
    Union,
    Literal,
    Any,
    Set,
)

from nextbeat.event_log import Event, EventLog, Timestamp
from nextbeat.scopes import ScopeValues
from nextbeat.topic_names import TopicName
from nextbeat.jobs import Actions, Job, JobPayload, JobRunner
from nextbeat.local_job_runner import LocalJobRunner
from nextbeat.time_event_publisher import (
    TimeEventPublisher,
    create_time_event_state_predicates,
    create_time_event_filters,
)
from nextbeat.topic import Action, Topic, StatePredicate, EventFilter
from nextbeat.effects import NextdbDynamicDependency
from nextdb.connection import ConnectionKey


def _get_jobs_or_scopes_from_result(
    result: Any,
) -> Union[
    Tuple[Literal["jobs"], Sequence[Job]],
    Tuple[Literal["scopes"], Sequence[ScopeValues]],
    Tuple[Literal["none"], None],
]:
    """
    If a job returns Job definitions or ScopeValues, we need to add those jobs/scopes to
    the scheduler. This function inspects a job's result to figure out if there are
    jobs/scopes that we need to add. Return types are hopefully clear from the type
    signature.
    """
    if isinstance(result, Job):
        return "jobs", [result]
    elif isinstance(result, ScopeValues):
        return "scopes", [result]
    elif isinstance(result, (list, tuple)) and len(result) > 0:
        # We don't want to just iterate through every Iterable we get back, iterating
        # through those Iterables could have side effects. Seems fine to only accept
        # lists and tuples.
        element_type = None
        for r in result:
            if isinstance(r, Job):
                if element_type is None:
                    element_type = "job"
                elif element_type == "job":
                    pass
                else:
                    # this means we have incompatible types
                    return "none", None
            elif isinstance(r, ScopeValues):
                if element_type is None:
                    element_type = "scope"
                elif element_type == "scope":
                    pass
                else:
                    # this means we have incompatible types
                    return "none", None
            else:
                # this means we have a non-job or non-scope in our iterable
                return "none", None
        if element_type == "job":
            return "jobs", result
        elif element_type == "scope":
            return "scopes", result
        else:
            # this should never happen, but probably better to be defensive here
            return "none", None
    else:
        return "none", None


@dataclasses.dataclass
class NextdbDependencyAction:
    """
    Scheduler creates one of these for each NextdbDynamicDependency that we see, as they
    require keeping some state in order to trigger them correctly
    """

    # These should be frozen, they tell us how to trigger the action. E.g. if we have a
    # Job that has a trigger_action that has a NextdbDependencyAction as one of its
    # wake_ons, we'll save the Job, TriggerAction.state_predicate, and
    # TriggerAction.action here so we know how/whether to trigger the action.
    job: Job
    action: Action
    state_predicate: StatePredicate

    # This holds state, "what tables did this job read the last time it ran". If any of
    # these tables get written to, that means we should trigger the job/action that this
    # NextdbDependencyAction represents.
    latest_tables_read: Optional[Set[Tuple[ConnectionKey, Tuple[str, str]]]] = None


class Scheduler:
    """
    A scheduler gets set up with jobs, and then executes actions on jobs as per the
    triggers defined on those jobs.

    TODO there are a lot of weird assumptions about what's called "on the event loop" vs
     from outside of it/on a different thread and what's threadsafe
    """

    _JOB_RUNNER_POLL_DELAY_SECONDS: float = 1

    def __init__(
        self,
        event_loop: Optional[asyncio.AbstractEventLoop] = None,
        job_runner_poll_delay_seconds: float = _JOB_RUNNER_POLL_DELAY_SECONDS,
    ) -> None:
        """
        job_runner_poll_delay_seconds is primarily to make unit tests run faster.
        """

        # the asyncio event_loop that we will use
        if event_loop is not None:
            self._event_loop: asyncio.AbstractEventLoop = event_loop
        else:
            self._event_loop: asyncio.AbstractEventLoop = asyncio.new_event_loop()
        # we hang onto these tasks to allow for graceful shutdown
        self._main_loop_task: Optional[Task[None]] = None
        self._time_event_publisher_task: Optional[Task[None]] = None

        # the event log stores events and lets us subscribe to events
        self._event_log: EventLog = EventLog(self._event_loop)
        # the TimeEventPublisher enables users to create time-based triggers, and
        # creates the right events at the right time.
        self.time: TimeEventPublisher = TimeEventPublisher(
            self._event_loop, self._event_log.append_event
        )

        # create the effects subscriber
        self._event_log.subscribe(None, self._process_effects)

        # all jobs that have been added to this scheduler
        self._jobs: Dict[TopicName, Job] = {}
        # the list of jobs that we've added but haven't created subscriptions for yet,
        # see create_job_subscriptions docstring. Only used temporarily when adding jobs
        self._create_job_subscriptions_queue: List[Job] = []
        # see comment on NextdbDependencyAction, this allows us to implement
        # NextdbDynamicDependency
        self._nextdb_dependencies: Dict[TopicName, NextdbDependencyAction] = {}

        # The local job runner is a special job runner that runs on the same machine as
        # nextbeat via multiprocessing.
        self._local_job_runner: LocalJobRunner = LocalJobRunner(self._event_log)
        # all job runners that have been added to this scheduler
        self._job_runners: List[JobRunner] = [self._local_job_runner]
        # how frequently to poll the job runners
        self._job_runner_poll_delay_seconds: float = job_runner_poll_delay_seconds

    def register_job_runner(
        self, job_runner_constructor: Callable[[EventLog], JobRunner]
    ) -> None:
        """
        Registers the job runner with the scheduler. As with manual_run, all this does
        is schedule a callback on the event_loop, so it's possible no state has changed
        when this function returns.
        """
        self._event_loop.call_soon_threadsafe(
            self.register_job_runner_on_event_loop, job_runner_constructor
        )

    def register_job_runner_on_event_loop(
        self, job_runner_constructor: Callable[[EventLog], JobRunner]
    ) -> None:
        """
        Registers the job runner with the scheduler. Must be run on self._event_loop.

        TODO add graceful shutdown, deal with job runners going offline, etc.
        """
        if asyncio.get_running_loop() != self._event_loop:
            raise ValueError(
                "Scheduler.register_job_runner_async was called from a different "
                "_event_loop than expected"
            )

        self._job_runners.append(job_runner_constructor(self._event_log))

    def add_job(self, job: Job) -> None:
        """
        Note that create_job_subscriptions needs to be called separately (see
        docstring).
        """
        if job.name in self._jobs:
            raise ValueError(f"Job with name {job.name} already exists.")
        self._jobs[job.name] = job
        self._create_job_subscriptions_queue.append(job)
        self._event_log.append_event(job.name, JobPayload(None, "WAITING"))

    def create_job_subscriptions(self) -> None:
        """
        Should be called after all jobs are added.

        Adding jobs and creating subscriptions is done in two phases to avoid order
        dependence (otherwise can't add a job that triggers based on another without
        adding the other first), and allows even circular dependencies. I.e. add_job
        should be called (repeatedly), then create_job_subscriptions should be called.
        """

        # TODO: this should also check the new jobs' preconditions against the existing
        #  state. Perhaps they should already trigger.
        # TODO: should make sure we don't try to proceed without calling
        #  create_job_subscriptions first
        for job in self._create_job_subscriptions_queue:
            job.all_subscribed_topics = []
            for trigger_action in job.trigger_actions:
                # this registers time events in the StatePredicate with our
                # TimeEventPublisher so that it knows we need to trigger at those times
                condition = create_time_event_state_predicates(
                    self.time, trigger_action.state_predicate
                )

                for event_filter in trigger_action.wake_on:
                    # this registers time events in the EventFilter with our
                    # TimeEventPublisher so that it knows we need to trigger at those
                    # times.
                    event_filter = create_time_event_filters(self.time, event_filter)

                    if isinstance(event_filter, NextdbDynamicDependency):
                        # This implements NextdbDynamicDependency, which can't be
                        # implemented as a normal subscriber, and instead is taken care
                        # of in _process_effects
                        # TODO hopefully no one creates multiple of these on the same
                        #  trigger action, we should probably throw an error in that
                        #  case
                        self._nextdb_dependencies[job.name] = NextdbDependencyAction(
                            job, trigger_action.action, trigger_action.state_predicate
                        )
                    else:

                        async def subscriber(
                            low_timestamp: Timestamp,
                            high_timestamp: Timestamp,
                            # to avoid capturing loop variables
                            job: Job = job,
                            event_filter: EventFilter = event_filter,
                            condition: StatePredicate = condition,
                            action: Action = trigger_action.action,
                        ) -> None:
                            # first check that there's at least one event that passes
                            # the EventFilter
                            if any(
                                event_filter.apply(event)
                                for topic_name in event_filter.topic_names_to_subscribe()
                                for event in self._event_log.events(
                                    topic_name, low_timestamp, high_timestamp
                                )
                            ):
                                # then check that the condition is met and if so execute
                                # the action
                                await self._action_if_predicate(
                                    job,
                                    condition,
                                    action,
                                    low_timestamp,
                                    high_timestamp,
                                )

                        # TODO we should consider throwing an exception if the topic
                        #  does not already exist (otherwise there's actually no point
                        #  in breaking out this create_job_subscriptions into a separate
                        #  function)
                        self._event_log.subscribe(
                            event_filter.topic_names_to_subscribe(), subscriber
                        )

                        # TODO would be nice to somehow get the dynamically subscribed
                        #  "topics" into all_subscribed_topics as well somehow...

                        job.all_subscribed_topics.extend(
                            event_filter.topic_names_to_subscribe()
                        )
                job.all_subscribed_topics.extend(condition.topic_names_to_query())
        self._create_job_subscriptions_queue.clear()

    async def _action_if_predicate(
        self,
        job: Job,
        condition: StatePredicate,
        action: Action,
        low_timestamp: Timestamp,
        high_timestamp: Timestamp,
    ) -> None:
        """Execute the action on the job if the condition is met."""

        events: Dict[TopicName, Tuple[Event, ...]] = {}
        for name in condition.topic_names_to_query():
            events[name] = tuple(
                self._event_log.events_and_state(name, low_timestamp, high_timestamp)
            )
        if condition.apply(events):
            await action.execute(
                job,
                self._job_runners,
                self._event_log,
                high_timestamp,
            )

    def add_jobs(self, jobs: Iterable[Job]) -> None:
        for job in jobs:
            self.add_job(job)
        self.create_job_subscriptions()

    def instantiate_scope(self, scope: ScopeValues) -> None:
        self._event_log.append_event(scope.topic_name(), scope)

    async def _process_effects(
        self, low_timestamp: Timestamp, high_timestamp: Timestamp
    ) -> None:
        """
        Should get called for all events. Idea is to react to effects in Job-related
        events
        """

        futures: List[Awaitable] = []

        # we want to iterate through events oldest first
        for event in reversed(
            list(self._event_log.events(None, low_timestamp, high_timestamp))
        ):
            if isinstance(event.payload, JobPayload):
                if event.payload.state == "SUCCEEDED":
                    # Adding jobs and instantiating scopes isn't a normal effect in
                    # terms of getting added to nextbeat.effects (that would be weird
                    # because they would only get "actioned" after the job completes).
                    # Instead, they get returned by the function but it makes sense to
                    # process them here as well. So here we check if results is Job,
                    # ScopeValues, or a list/tuple of those, and add them to the
                    # scheduler

                    result_type, result = _get_jobs_or_scopes_from_result(
                        event.payload.result_value
                    )
                    if result_type == "jobs":
                        self.add_jobs(result)
                    elif result_type == "scopes":
                        for scope in result:
                            self.instantiate_scope(scope)
                    elif result_type == "none":
                        pass
                    else:
                        raise ValueError(
                            "Internal error, got an unexpected result_type "
                            f"{result_type}"
                        )

                    # Now process nextdb_effects
                    # TODO Some effects (i.e. writes) should probably still be processed
                    #  even if the job was not successful.
                    futures.extend(
                        self._process_nextdb_effects(
                            event, low_timestamp, high_timestamp
                        )
                    )

        await asyncio.gather(*futures)

    def _process_nextdb_effects(
        self,
        event: Event[JobPayload],
        low_timestamp: Timestamp,
        high_timestamp: Timestamp,
    ) -> Iterable[Awaitable]:
        """
        Processes the NextdbEffects on event (if any). Updates self._nextdb_dependencies
        with reads and executes any actions on writes. Returns the futures created from
        executing the actions (if any).
        """
        # TODO this implementation is probably overly simplistic. Consider scenarios:
        # J, K, I are jobs, T, U are tables
        # 1. In this batch of events, K writes to T, then J reads from T, then J runs
        #    again and reads from U and not T. Should J be triggered again? (Also, is
        #    weird that J can "stop" reading from U, this probably deserves some
        #    thought.)
        # 2. J reads from T, K writes to T, then I writes to T. Should J be triggered
        #    once or twice?
        # 3. K writes to T, J reads from T. Should J be triggered again? Answer to this
        #    one is to check if the last run of J read the version that K wrote
        # Probably will be more efficient to process all of the events in the
        # _process_effects batch together depending on the exact semantics we go with.
        # Even outside of a batch of events, keep in mind that the order we see the
        # events for jobs completing actually has no relationship to when those jobs
        # read particular tables. E.g. all 4 combinations of "J read T before K wrote to
        # T"/"K wrote to T before J read T", and "J finishes before K"/"K finishes
        # before J" are possible.

        if event.payload.effects is not None:
            # if a job has a dynamic nextdb dependency and it just ran, we need to
            # update its table dependencies to be whatever it just read
            if event.topic_name in self._nextdb_dependencies:
                reads = set(
                    (conn, table)
                    for conn, effects in event.payload.effects.nextdb_effects.items()
                    for table in effects.tables_read.keys()
                )
                if len(reads) == 0:
                    # TODO this should probably do more than just warn
                    print(
                        f"Job {event.topic_name} with dynamic nextdb dependencies did "
                        "not read any nextdb tables, dynamic dependencies will not be "
                        "triggered again until the job is rerun"
                    )
                self._nextdb_dependencies[event.topic_name].latest_tables_read = reads

            # now trigger jobs based on writes
            writes = set(
                (conn, table)
                for conn, effects in event.payload.effects.nextdb_effects.items()
                for table in effects.tables_written.keys()
            )
            if writes:
                for nextdb_dependency in self._nextdb_dependencies.values():
                    if (
                        nextdb_dependency.latest_tables_read is not None
                        and nextdb_dependency.latest_tables_read.intersection(writes)
                    ):
                        yield self._action_if_predicate(
                            nextdb_dependency.job,
                            nextdb_dependency.state_predicate,
                            nextdb_dependency.action,
                            low_timestamp,
                            high_timestamp,
                        )

    def manual_run(self, job_name: TopicName) -> None:
        """
        Execute the Run Action on the specified job.

        Important--when this function returns, it's possible that no events have been
        created yet, not even RUN_REQUESTED.
        """
        if job_name not in self._jobs:
            raise ValueError(f"Unknown job: {job_name}")
        job = self._jobs[job_name]
        self._event_loop.call_soon_threadsafe(
            lambda: self._event_loop.create_task(self._run_action(job, Actions.run))
        )

    async def manual_run_on_event_loop(self, job_name: TopicName) -> None:
        """Execute the Run Action on the specified job."""
        # TODO see if we can eliminate a little copy/paste here
        if job_name not in self._jobs:
            raise ValueError(f"Unknown job: {job_name}")
        job = self._jobs[job_name]
        await self._run_action(job, Actions.run)

    async def _run_action(self, topic: Topic, action: Action) -> None:
        try:
            await action.execute(
                topic,
                self._job_runners,
                self._event_log,
                self._event_log.curr_timestamp,
            )
        except Exception:
            # TODO this function isn't awaited, so exceptions need to make it back into
            #  the scheduler somehow
            traceback.print_exc()

    def _get_running_and_requested_jobs(self) -> Iterable[Event[JobPayload]]:
        """
        Returns the latest event for any job that's in RUN_REQUESTED or RUNNING state
        """
        timestamp = self._event_log.curr_timestamp
        for name in self._jobs.keys():
            ev = self._event_log.last_event(name, timestamp)
            if ev and ev.payload.state in ("RUN_REQUESTED", "RUNNING"):
                yield ev

    async def _poll_job_runners_loop(self) -> None:
        """Periodically polls the job runners we know about"""
        while True:
            try:
                # TODO should we keep track of which jobs are running on which job
                #  runner and only poll for those jobs?
                last_events = list(self._get_running_and_requested_jobs())
                await asyncio.gather(
                    *[jr.poll_jobs(last_events) for jr in self._job_runners]
                )
            except Exception:
                # TODO do something smarter here...
                traceback.print_exc()
            await asyncio.sleep(self._job_runner_poll_delay_seconds)

    def get_main_loop_tasks(self) -> Iterable[Awaitable]:
        yield self._event_loop.create_task(self._poll_job_runners_loop())
        yield self._event_loop.create_task(self.time.main_loop())
        yield self._event_loop.create_task(self._event_log.call_subscribers_loop())

    def main_loop(self) -> threading.Thread:
        """
        This starts a daemon (background) thread that runs forever. This code just polls
        the job runners, but other code will add callbacks to run on this event loop
        (e.g. EventLog.call_subscribers).

        TODO not clear that this is really necessary anymore
        """

        t = threading.Thread(
            target=lambda: self._event_loop.run_until_complete(
                asyncio.wait(list(self.get_main_loop_tasks()))
            ),
            daemon=True,
        )
        t.start()
        return t

    def shutdown(self) -> None:
        if self._main_loop_task is not None:
            self._main_loop_task.cancel()
            self._time_event_publisher_task.cancel()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()

    def all_are_waiting(self) -> bool:
        """
        Returns true if everything is in a "waiting" state. I.e. no jobs are running,
        all subscribers have been processed.
        """
        return self._event_log.all_subscribers_called() and not any(
            True for _ in self._get_running_and_requested_jobs()
        )

    def events_of(self, topic_name: TopicName) -> List[Event]:
        """For unit tests/debugging"""
        return list(
            self._event_log.events_and_state(
                topic_name, 0, self._event_log.curr_timestamp
            )
        )
