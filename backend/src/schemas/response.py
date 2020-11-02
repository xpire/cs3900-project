from functools import wraps
from typing import Any, Optional

from pydantic import BaseModel as BaseSchema
from src.core.utilities import HTTP400, log_msg


class Response(BaseSchema):
    """
    Generic API response type
    """

    msg: str


class Result(BaseSchema):
    """
    Internal return type
    """

    msg: str = ""
    success: bool
    data: Optional[Any]

    def log(self, log_level=None):
        if self.success:
            log_level = log_level or "INFO"
        else:
            log_level = log_level or "ERROR"

        log_msg(self.msg, log_level)
        return self

    def as_response(self):
        if self.success:
            return Response(msg=self.msg)
        else:
            raise HTTP400(self.msg)

    def assert_ok(self):
        if not self.success:
            raise ResultException(self)

    def __bool__(self):
        return self.success


def get_result_maker(success):
    def result_maker(msg="", data=None) -> Result:
        if data is None:
            return Result(msg=msg, success=success)
        else:
            return Result(msg=msg, success=success, data=data)

    return result_maker


Success = get_result_maker(True)
Fail = get_result_maker(False)


class ResultException(Exception):
    def __init__(self, result):
        super().__init__()
        self.result = result


# Coded based on: https://stackoverflow.com/questions/42043226/using-a-coroutine-as-decorator
def return_response():
    def wrapper(fn):
        @wraps(fn)
        async def wrapped(*args, **kwargs) -> Response:
            return (await fn(*args, **kwargs)).as_response()

        return wrapped

    return wrapper


def return_result():
    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs) -> Result:
            try:
                res = fn(*args, **kwargs)
                return Success() if res is None else res
            except ResultException as e:
                return e.result

        return wrapped

    return wrapper
