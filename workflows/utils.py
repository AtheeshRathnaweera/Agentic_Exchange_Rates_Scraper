import asyncio


def wrap_executor(executor_fn):
    """
    Wraps an executor function to handle workflow termination.

    If the wrapped function returns an object with a 'stop' attribute set to True,
    an Exception is raised with the 'content' attribute as the message (or a default message).

    Supports both synchronous and asynchronous executor functions.

    Args:
        executor_fn (Callable): The function to wrap.

    Returns:
        Callable: A wrapped function that raises an exception if workflow termination is signaled.
    """

    async def async_wrapper(*args, **kwargs):
        result = await executor_fn(*args, **kwargs)
        if getattr(result, "stop", False):
            msg = getattr(result, "content", "Workflow terminated by step")
            raise Exception(msg)
        return result

    def sync_wrapper(*args, **kwargs):
        result = executor_fn(*args, **kwargs)
        if getattr(result, "stop", False):
            msg = getattr(result, "content", "Workflow terminated by step")
            raise Exception(msg)
        return result

    return async_wrapper if asyncio.iscoroutinefunction(executor_fn) else sync_wrapper
