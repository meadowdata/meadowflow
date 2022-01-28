# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc

from meadowgrid import meadowgrid_pb2 as meadowgrid_dot_meadowgrid__pb2


class MeadowGridCoordinatorStub(object):
    """client functions"""

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.add_job = channel.unary_unary(
            "/meadowgrid.MeadowGridCoordinator/add_job",
            request_serializer=meadowgrid_dot_meadowgrid__pb2.Job.SerializeToString,
            response_deserializer=meadowgrid_dot_meadowgrid__pb2.AddJobResponse.FromString,
        )
        self.add_tasks_to_grid_job = channel.unary_unary(
            "/meadowgrid.MeadowGridCoordinator/add_tasks_to_grid_job",
            request_serializer=meadowgrid_dot_meadowgrid__pb2.AddTasksToGridJobRequest.SerializeToString,
            response_deserializer=meadowgrid_dot_meadowgrid__pb2.AddJobResponse.FromString,
        )
        self.get_simple_job_states = channel.unary_unary(
            "/meadowgrid.MeadowGridCoordinator/get_simple_job_states",
            request_serializer=meadowgrid_dot_meadowgrid__pb2.JobStatesRequest.SerializeToString,
            response_deserializer=meadowgrid_dot_meadowgrid__pb2.ProcessStates.FromString,
        )
        self.get_grid_task_states = channel.unary_unary(
            "/meadowgrid.MeadowGridCoordinator/get_grid_task_states",
            request_serializer=meadowgrid_dot_meadowgrid__pb2.GridTaskStatesRequest.SerializeToString,
            response_deserializer=meadowgrid_dot_meadowgrid__pb2.GridTaskStatesResponse.FromString,
        )
        self.add_credentials = channel.unary_unary(
            "/meadowgrid.MeadowGridCoordinator/add_credentials",
            request_serializer=meadowgrid_dot_meadowgrid__pb2.AddCredentialsRequest.SerializeToString,
            response_deserializer=meadowgrid_dot_meadowgrid__pb2.AddCredentialsResponse.FromString,
        )
        self.get_agent_states = channel.unary_unary(
            "/meadowgrid.MeadowGridCoordinator/get_agent_states",
            request_serializer=meadowgrid_dot_meadowgrid__pb2.AgentStatesRequest.SerializeToString,
            response_deserializer=meadowgrid_dot_meadowgrid__pb2.AgentStatesResponse.FromString,
        )
        self.register_agent = channel.unary_unary(
            "/meadowgrid.MeadowGridCoordinator/register_agent",
            request_serializer=meadowgrid_dot_meadowgrid__pb2.RegisterAgentRequest.SerializeToString,
            response_deserializer=meadowgrid_dot_meadowgrid__pb2.RegisterAgentResponse.FromString,
        )
        self.get_next_jobs = channel.unary_unary(
            "/meadowgrid.MeadowGridCoordinator/get_next_jobs",
            request_serializer=meadowgrid_dot_meadowgrid__pb2.NextJobsRequest.SerializeToString,
            response_deserializer=meadowgrid_dot_meadowgrid__pb2.NextJobsResponse.FromString,
        )
        self.update_job_states = channel.unary_unary(
            "/meadowgrid.MeadowGridCoordinator/update_job_states",
            request_serializer=meadowgrid_dot_meadowgrid__pb2.JobStateUpdates.SerializeToString,
            response_deserializer=meadowgrid_dot_meadowgrid__pb2.UpdateStateResponse.FromString,
        )
        self.update_grid_task_state_and_get_next = channel.unary_unary(
            "/meadowgrid.MeadowGridCoordinator/update_grid_task_state_and_get_next",
            request_serializer=meadowgrid_dot_meadowgrid__pb2.GridTaskUpdateAndGetNextRequest.SerializeToString,
            response_deserializer=meadowgrid_dot_meadowgrid__pb2.GridTask.FromString,
        )
        self.Check = channel.unary_unary(
            "/meadowgrid.MeadowGridCoordinator/Check",
            request_serializer=meadowgrid_dot_meadowgrid__pb2.HealthCheckRequest.SerializeToString,
            response_deserializer=meadowgrid_dot_meadowgrid__pb2.HealthCheckResponse.FromString,
        )


class MeadowGridCoordinatorServicer(object):
    """client functions"""

    def add_job(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def add_tasks_to_grid_job(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def get_simple_job_states(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def get_grid_task_states(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def add_credentials(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def get_agent_states(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def register_agent(self, request, context):
        """agent/worker functions"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def get_next_jobs(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def update_job_states(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def update_grid_task_state_and_get_next(self, request, context):
        """this can only get tasks from the same job"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")

    def Check(self, request, context):
        """per convention: https://github.com/grpc/grpc/blob/master/doc/health-checking.md"""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details("Method not implemented!")
        raise NotImplementedError("Method not implemented!")


def add_MeadowGridCoordinatorServicer_to_server(servicer, server):
    rpc_method_handlers = {
        "add_job": grpc.unary_unary_rpc_method_handler(
            servicer.add_job,
            request_deserializer=meadowgrid_dot_meadowgrid__pb2.Job.FromString,
            response_serializer=meadowgrid_dot_meadowgrid__pb2.AddJobResponse.SerializeToString,
        ),
        "add_tasks_to_grid_job": grpc.unary_unary_rpc_method_handler(
            servicer.add_tasks_to_grid_job,
            request_deserializer=meadowgrid_dot_meadowgrid__pb2.AddTasksToGridJobRequest.FromString,
            response_serializer=meadowgrid_dot_meadowgrid__pb2.AddJobResponse.SerializeToString,
        ),
        "get_simple_job_states": grpc.unary_unary_rpc_method_handler(
            servicer.get_simple_job_states,
            request_deserializer=meadowgrid_dot_meadowgrid__pb2.JobStatesRequest.FromString,
            response_serializer=meadowgrid_dot_meadowgrid__pb2.ProcessStates.SerializeToString,
        ),
        "get_grid_task_states": grpc.unary_unary_rpc_method_handler(
            servicer.get_grid_task_states,
            request_deserializer=meadowgrid_dot_meadowgrid__pb2.GridTaskStatesRequest.FromString,
            response_serializer=meadowgrid_dot_meadowgrid__pb2.GridTaskStatesResponse.SerializeToString,
        ),
        "add_credentials": grpc.unary_unary_rpc_method_handler(
            servicer.add_credentials,
            request_deserializer=meadowgrid_dot_meadowgrid__pb2.AddCredentialsRequest.FromString,
            response_serializer=meadowgrid_dot_meadowgrid__pb2.AddCredentialsResponse.SerializeToString,
        ),
        "get_agent_states": grpc.unary_unary_rpc_method_handler(
            servicer.get_agent_states,
            request_deserializer=meadowgrid_dot_meadowgrid__pb2.AgentStatesRequest.FromString,
            response_serializer=meadowgrid_dot_meadowgrid__pb2.AgentStatesResponse.SerializeToString,
        ),
        "register_agent": grpc.unary_unary_rpc_method_handler(
            servicer.register_agent,
            request_deserializer=meadowgrid_dot_meadowgrid__pb2.RegisterAgentRequest.FromString,
            response_serializer=meadowgrid_dot_meadowgrid__pb2.RegisterAgentResponse.SerializeToString,
        ),
        "get_next_jobs": grpc.unary_unary_rpc_method_handler(
            servicer.get_next_jobs,
            request_deserializer=meadowgrid_dot_meadowgrid__pb2.NextJobsRequest.FromString,
            response_serializer=meadowgrid_dot_meadowgrid__pb2.NextJobsResponse.SerializeToString,
        ),
        "update_job_states": grpc.unary_unary_rpc_method_handler(
            servicer.update_job_states,
            request_deserializer=meadowgrid_dot_meadowgrid__pb2.JobStateUpdates.FromString,
            response_serializer=meadowgrid_dot_meadowgrid__pb2.UpdateStateResponse.SerializeToString,
        ),
        "update_grid_task_state_and_get_next": grpc.unary_unary_rpc_method_handler(
            servicer.update_grid_task_state_and_get_next,
            request_deserializer=meadowgrid_dot_meadowgrid__pb2.GridTaskUpdateAndGetNextRequest.FromString,
            response_serializer=meadowgrid_dot_meadowgrid__pb2.GridTask.SerializeToString,
        ),
        "Check": grpc.unary_unary_rpc_method_handler(
            servicer.Check,
            request_deserializer=meadowgrid_dot_meadowgrid__pb2.HealthCheckRequest.FromString,
            response_serializer=meadowgrid_dot_meadowgrid__pb2.HealthCheckResponse.SerializeToString,
        ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
        "meadowgrid.MeadowGridCoordinator", rpc_method_handlers
    )
    server.add_generic_rpc_handlers((generic_handler,))


# This class is part of an EXPERIMENTAL API.
class MeadowGridCoordinator(object):
    """client functions"""

    @staticmethod
    def add_job(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/meadowgrid.MeadowGridCoordinator/add_job",
            meadowgrid_dot_meadowgrid__pb2.Job.SerializeToString,
            meadowgrid_dot_meadowgrid__pb2.AddJobResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def add_tasks_to_grid_job(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/meadowgrid.MeadowGridCoordinator/add_tasks_to_grid_job",
            meadowgrid_dot_meadowgrid__pb2.AddTasksToGridJobRequest.SerializeToString,
            meadowgrid_dot_meadowgrid__pb2.AddJobResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def get_simple_job_states(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/meadowgrid.MeadowGridCoordinator/get_simple_job_states",
            meadowgrid_dot_meadowgrid__pb2.JobStatesRequest.SerializeToString,
            meadowgrid_dot_meadowgrid__pb2.ProcessStates.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def get_grid_task_states(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/meadowgrid.MeadowGridCoordinator/get_grid_task_states",
            meadowgrid_dot_meadowgrid__pb2.GridTaskStatesRequest.SerializeToString,
            meadowgrid_dot_meadowgrid__pb2.GridTaskStatesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def add_credentials(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/meadowgrid.MeadowGridCoordinator/add_credentials",
            meadowgrid_dot_meadowgrid__pb2.AddCredentialsRequest.SerializeToString,
            meadowgrid_dot_meadowgrid__pb2.AddCredentialsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def get_agent_states(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/meadowgrid.MeadowGridCoordinator/get_agent_states",
            meadowgrid_dot_meadowgrid__pb2.AgentStatesRequest.SerializeToString,
            meadowgrid_dot_meadowgrid__pb2.AgentStatesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def register_agent(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/meadowgrid.MeadowGridCoordinator/register_agent",
            meadowgrid_dot_meadowgrid__pb2.RegisterAgentRequest.SerializeToString,
            meadowgrid_dot_meadowgrid__pb2.RegisterAgentResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def get_next_jobs(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/meadowgrid.MeadowGridCoordinator/get_next_jobs",
            meadowgrid_dot_meadowgrid__pb2.NextJobsRequest.SerializeToString,
            meadowgrid_dot_meadowgrid__pb2.NextJobsResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def update_job_states(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/meadowgrid.MeadowGridCoordinator/update_job_states",
            meadowgrid_dot_meadowgrid__pb2.JobStateUpdates.SerializeToString,
            meadowgrid_dot_meadowgrid__pb2.UpdateStateResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def update_grid_task_state_and_get_next(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/meadowgrid.MeadowGridCoordinator/update_grid_task_state_and_get_next",
            meadowgrid_dot_meadowgrid__pb2.GridTaskUpdateAndGetNextRequest.SerializeToString,
            meadowgrid_dot_meadowgrid__pb2.GridTask.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )

    @staticmethod
    def Check(
        request,
        target,
        options=(),
        channel_credentials=None,
        call_credentials=None,
        insecure=False,
        compression=None,
        wait_for_ready=None,
        timeout=None,
        metadata=None,
    ):
        return grpc.experimental.unary_unary(
            request,
            target,
            "/meadowgrid.MeadowGridCoordinator/Check",
            meadowgrid_dot_meadowgrid__pb2.HealthCheckRequest.SerializeToString,
            meadowgrid_dot_meadowgrid__pb2.HealthCheckResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
        )
