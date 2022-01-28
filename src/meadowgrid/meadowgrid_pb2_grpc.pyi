"""
@generated by mypy-protobuf.  Do not edit manually!
isort:skip_file
"""
import abc
import grpc
import meadowgrid.meadowgrid_pb2

class MeadowGridCoordinatorStub:
    """client functions"""

    def __init__(self, channel: grpc.Channel) -> None: ...
    add_job: grpc.UnaryUnaryMultiCallable[
        meadowgrid.meadowgrid_pb2.Job, meadowgrid.meadowgrid_pb2.AddJobResponse
    ] = ...

    add_tasks_to_grid_job: grpc.UnaryUnaryMultiCallable[
        meadowgrid.meadowgrid_pb2.AddTasksToGridJobRequest,
        meadowgrid.meadowgrid_pb2.AddJobResponse,
    ] = ...

    get_simple_job_states: grpc.UnaryUnaryMultiCallable[
        meadowgrid.meadowgrid_pb2.JobStatesRequest,
        meadowgrid.meadowgrid_pb2.ProcessStates,
    ] = ...

    get_grid_task_states: grpc.UnaryUnaryMultiCallable[
        meadowgrid.meadowgrid_pb2.GridTaskStatesRequest,
        meadowgrid.meadowgrid_pb2.GridTaskStatesResponse,
    ] = ...

    add_credentials: grpc.UnaryUnaryMultiCallable[
        meadowgrid.meadowgrid_pb2.AddCredentialsRequest,
        meadowgrid.meadowgrid_pb2.AddCredentialsResponse,
    ] = ...

    get_agent_states: grpc.UnaryUnaryMultiCallable[
        meadowgrid.meadowgrid_pb2.AgentStatesRequest,
        meadowgrid.meadowgrid_pb2.AgentStatesResponse,
    ] = ...

    register_agent: grpc.UnaryUnaryMultiCallable[
        meadowgrid.meadowgrid_pb2.RegisterAgentRequest,
        meadowgrid.meadowgrid_pb2.RegisterAgentResponse,
    ] = ...
    """agent/worker functions

    """

    get_next_jobs: grpc.UnaryUnaryMultiCallable[
        meadowgrid.meadowgrid_pb2.NextJobsRequest,
        meadowgrid.meadowgrid_pb2.NextJobsResponse,
    ] = ...

    update_job_states: grpc.UnaryUnaryMultiCallable[
        meadowgrid.meadowgrid_pb2.JobStateUpdates,
        meadowgrid.meadowgrid_pb2.UpdateStateResponse,
    ] = ...

    update_grid_task_state_and_get_next: grpc.UnaryUnaryMultiCallable[
        meadowgrid.meadowgrid_pb2.GridTaskUpdateAndGetNextRequest,
        meadowgrid.meadowgrid_pb2.GridTask,
    ] = ...
    """this can only get tasks from the same job"""

    Check: grpc.UnaryUnaryMultiCallable[
        meadowgrid.meadowgrid_pb2.HealthCheckRequest,
        meadowgrid.meadowgrid_pb2.HealthCheckResponse,
    ] = ...
    """per convention: https://github.com/grpc/grpc/blob/master/doc/health-checking.md"""

class MeadowGridCoordinatorServicer(metaclass=abc.ABCMeta):
    """client functions"""

    @abc.abstractmethod
    def add_job(
        self,
        request: meadowgrid.meadowgrid_pb2.Job,
        context: grpc.ServicerContext,
    ) -> meadowgrid.meadowgrid_pb2.AddJobResponse: ...
    @abc.abstractmethod
    def add_tasks_to_grid_job(
        self,
        request: meadowgrid.meadowgrid_pb2.AddTasksToGridJobRequest,
        context: grpc.ServicerContext,
    ) -> meadowgrid.meadowgrid_pb2.AddJobResponse: ...
    @abc.abstractmethod
    def get_simple_job_states(
        self,
        request: meadowgrid.meadowgrid_pb2.JobStatesRequest,
        context: grpc.ServicerContext,
    ) -> meadowgrid.meadowgrid_pb2.ProcessStates: ...
    @abc.abstractmethod
    def get_grid_task_states(
        self,
        request: meadowgrid.meadowgrid_pb2.GridTaskStatesRequest,
        context: grpc.ServicerContext,
    ) -> meadowgrid.meadowgrid_pb2.GridTaskStatesResponse: ...
    @abc.abstractmethod
    def add_credentials(
        self,
        request: meadowgrid.meadowgrid_pb2.AddCredentialsRequest,
        context: grpc.ServicerContext,
    ) -> meadowgrid.meadowgrid_pb2.AddCredentialsResponse: ...
    @abc.abstractmethod
    def get_agent_states(
        self,
        request: meadowgrid.meadowgrid_pb2.AgentStatesRequest,
        context: grpc.ServicerContext,
    ) -> meadowgrid.meadowgrid_pb2.AgentStatesResponse: ...
    @abc.abstractmethod
    def register_agent(
        self,
        request: meadowgrid.meadowgrid_pb2.RegisterAgentRequest,
        context: grpc.ServicerContext,
    ) -> meadowgrid.meadowgrid_pb2.RegisterAgentResponse:
        """agent/worker functions"""
        pass
    @abc.abstractmethod
    def get_next_jobs(
        self,
        request: meadowgrid.meadowgrid_pb2.NextJobsRequest,
        context: grpc.ServicerContext,
    ) -> meadowgrid.meadowgrid_pb2.NextJobsResponse: ...
    @abc.abstractmethod
    def update_job_states(
        self,
        request: meadowgrid.meadowgrid_pb2.JobStateUpdates,
        context: grpc.ServicerContext,
    ) -> meadowgrid.meadowgrid_pb2.UpdateStateResponse: ...
    @abc.abstractmethod
    def update_grid_task_state_and_get_next(
        self,
        request: meadowgrid.meadowgrid_pb2.GridTaskUpdateAndGetNextRequest,
        context: grpc.ServicerContext,
    ) -> meadowgrid.meadowgrid_pb2.GridTask:
        """this can only get tasks from the same job"""
        pass
    @abc.abstractmethod
    def Check(
        self,
        request: meadowgrid.meadowgrid_pb2.HealthCheckRequest,
        context: grpc.ServicerContext,
    ) -> meadowgrid.meadowgrid_pb2.HealthCheckResponse:
        """per convention: https://github.com/grpc/grpc/blob/master/doc/health-checking.md"""
        pass

def add_MeadowGridCoordinatorServicer_to_server(
    servicer: MeadowGridCoordinatorServicer, server: grpc.Server
) -> None: ...
