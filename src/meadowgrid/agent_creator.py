from __future__ import annotations

import abc
import collections
from typing import Literal, Optional, Dict

import numpy as np
import pandas as pd

import meadowgrid.resource_allocation

AgentCreatorType = Literal["local", "aws", None]
OnDemandOrSpotType = Literal["on_demand", "spot"]


class AgentCreator(abc.ABC):
    """
    Implementations of this class are responsible for creating agents for the
    coordinator. Example implementations are AwsAgentCreator, LocalAgentCreator.
    """

    @abc.abstractmethod
    async def get_instance_types(self) -> Optional[pd.DataFrame]:
        """
        Gets information about the instance types that this AgentCreator is able to
        create.

        See choose_instance_types_for_job docstring for the schema of the returned
        DataFrame
        """
        pass

    @abc.abstractmethod
    async def launch_job_specific_agent(
        self,
        agent_id: str,
        job_id: str,
        instance_type: str,
        on_demand_or_spot: OnDemandOrSpotType,
    ) -> None:
        """
        Creates an instance of the specified instance_type with a meadowgrid agent
        running on it. job_id is passed as a parameter to the agent process.
        """
        pass

    @abc.abstractmethod
    async def close(self) -> None:
        """Equivalent of __aexit__"""
        pass

    # TODO we need to have a way to kill agents when we're done with them


def choose_instance_types_for_job(
    resources_required: meadowgrid.resource_allocation.Resources,
    num_workers_to_allocate: int,
    interruption_probability_threshold: float,
    instance_types: pd.DataFrame,
) -> pd.DataFrame:
    """
    This chooses how many of which instance types we should launch for a job with 1 or
    more tasks where each task requires resources_required so that num_tasks_to_allocate
    tasks can run in parallel. We choose the cheapest instances that have interruption
    probability lower than or equal to the specified threshold. If you only want to use
    on-demand instances that have 0 probability of interruption, you can set
    interruption_probability_threshold to 0. If there are multiple instances that are
    the cheapest, we choose the ones that have the lowest interruption probability. If
    there are still multiple instances, then we diversify among those instance types (it
    seems that interruptions are more likely to happen at the same time on the same
    instance types).

    instance_types should be a dataframe with these columns:
    - instance_type: str, e.g. t2.micro
    - memory_gb: float, e.g. 4 means 4 GiB
    - logical_cpu: int, e.g. 2 means 2 logical (aka virtual) cpus
    - price: float, e.g. 0.023 means 0.023 USD per hour to run the instance
    - interruption_probability: float, e.g. 0 for on-demand instances, >0 for spot
      instances, as a percentage, so values range from 0 to 100.
    - on_demand_or_spot: str, "on_demand" or "spot" (not used in this function)

    returns a dataframe with the same schema as instance_types, with additional columns:
    - num_instances: e.g. 5 means we should allocate 5 of these instances
    - workers_per_instance: how many workers should be able to run on that instance
    Rows (i.e. instance types) will only be present if num_instances is at least 1.

    TODO we should maybe have an option where e.g. if you want to allocate 53 workers
     worth of capacity for a 100-task job, it makes more sense to allocate e.g. 55 or 60
     workers worth of capacity rather than allocating a little machine for the last 3
     workers of capacity
    """

    # make a copy of instance_types, as we want to modify it in place
    instance_types = instance_types.copy()

    # ignore anything with a higher interruption probability than what we want to
    # tolerate
    instance_types = instance_types[
        instance_types["interruption_probability"] <= interruption_probability_threshold
    ]

    # the maximum number of workers we could pack onto each instance type
    instance_types["workers_per_instance"] = np.minimum(
        np.floor(instance_types["memory_gb"] / resources_required.memory_gb),
        np.floor(instance_types["logical_cpu"] / resources_required.logical_cpu),
    ).astype(int)
    # ignore instance types where we won't be able to fit even 1 worker
    instance_types = instance_types[instance_types["workers_per_instance"] >= 1]
    # if we get the maximum number of workers packed onto the instance type, what is our
    # effective price per worker
    instance_types["price_per_worker"] = (
        instance_types["price"] / instance_types["workers_per_instance"]
    )

    instance_types = instance_types.reset_index(drop=True)
    # This will keep track of how many of which instance type to use. E.g. {34: 5} tells
    # us to use 5 instances of the instance_types.loc[34] instance type
    instance_types_to_use: Dict[int, int] = collections.defaultdict(lambda: 0)

    while num_workers_to_allocate > 0:
        best = instance_types.copy()

        # for larger instances, there might not be enough num_workers_to_allocate to
        # make it "worth it" to use that larger instance because we won't have enough
        # workers to fully pack the instance. So we recompute price_per_worker for those
        # instances assuming we only get to put num_workers_to_allocate on that
        # instance.
        too_large_index = (
            instance_types["workers_per_instance"] > num_workers_to_allocate
        )
        best.loc[too_large_index, "price_per_worker"] = (
            best.loc[too_large_index, "price"] / num_workers_to_allocate
        )

        # Now find the instance types that have the lowest price per worker. If there
        # are multiple instance types that have the same price per worker (or are within
        # half a penny per hour), then take the ones that have the lowest probability of
        # interruption (within 1%)
        # TODO maybe the rounding should be configurable?
        best = best[(best["price_per_worker"] - best["price_per_worker"].min()) < 0.005]
        best = best[
            (best["interruption_probability"] - best["interruption_probability"].min())
            < 1
        ]

        # At this point, best is the set of instance types that are the cheapest and
        # least interruption-likely for our workload. Next, we'll make sure to take one,
        # so that we definitely make progress on allocating workers to instances. After
        # that, though, if we still have workers left to allocate, we want to allocate
        # them round-robin to the remaining instance types in best--the diversity in
        # instance types is good because instances of the same type are more likely to
        # get interrupted at the same time according to
        # https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/spot-fleet-allocation-strategy.html

        # iterating from largest to smallest will make things easier
        best = best.sort_values(["workers_per_instance"], ascending=False)

        # take the first one no matter what
        i = 0
        instance_types_to_use[best.index[i]] += 1
        num_workers_to_allocate -= best.loc[best.index[i], "workers_per_instance"]

        # Now that we've decreased num_workers_to_allocate, we need to make sure
        # price_per_worker is still accurate (i.e. num_workers_to_allocate could have
        # fallen below workers_per_instance). If there are any instance types that where
        # price_per_worker is still accurate, then we'll continue to allocate to those
        # in a round-robin-ish fashion. Once there are no more instance types where
        # price_per_worker is still accurate, we'll go through the loop again and
        # recompute price_per_worker.
        while True:
            best = best[best["workers_per_instance"] <= num_workers_to_allocate]
            if len(best) == 0:
                break
            # this is...very inexact because best is changing as we iterate, but the
            # idea is to walk through the options in best one by one
            i = (i + 1) % len(best)
            instance_types_to_use[best.index[i]] += 1
            num_workers_to_allocate -= best.loc[best.index[i], "workers_per_instance"]

    # relies on defaultdict.keys() and .values() iterating in the same order
    return instance_types.loc[instance_types_to_use.keys()].assign(
        num_instances=instance_types_to_use.values()
    )
