"""
This is code that "should" be part of ec2_alloc.py, but is also needed by
adjust_ec2_instances.

This module contains code that will run in the generic AWS Lambda environment, so it
should not refer to any outside code
"""
from __future__ import annotations

from typing import Callable, Tuple, Optional, TypeVar

import botocore.exceptions


_T = TypeVar("_T")

# a dynamodb table that holds information about EC2 instances we've created and what has
# been allocated to which instances
_EC2_ALLOC_TABLE_NAME = "_meadowgrid_ec2_alloc_table"

# names of attributes/keys in the EC2 alloc table
_PUBLIC_ADDRESS = "public_address"
_LOGICAL_CPU_AVAILABLE = "logical_cpu_available"
_LOGICAL_CPU_ALLOCATED = "logical_cpu_allocated"
_MEMORY_GB_AVAILABLE = "memory_gb_available"
_MEMORY_GB_ALLOCATED = "memory_gb_allocated"
_ALLOCATED_TIME = "allocated_time"
_LAST_UPDATE_TIME = "last_update_time"
_RUNNING_JOBS = "running_jobs"
_JOB_ID = "job_id"

# A tag for EC2 instances that are created using ec2_alloc
_EC2_ALLOC_TAG = "meadowgrid_ec2_alloc"
_EC2_ALLOC_TAG_VALUE = "TRUE"


def ignore_boto3_error_code(
    func: Callable[[], _T], error_code: str
) -> Tuple[bool, Optional[_T]]:
    """
    Calls func. If func succeeds, return (True, result of func). If func raises a boto3
    error with the specified code, returns False, None. If func raises any other type of
    exception (i.e. a boto3 error with a different code or a different type of error
    altogether), then the exception is raised normally.
    """
    try:
        return True, func()
    except botocore.exceptions.ClientError as e:
        if "Error" in e.response:
            error = e.response["Error"]
            if "Code" in error and error["Code"] == error_code:
                return False, None

        raise
