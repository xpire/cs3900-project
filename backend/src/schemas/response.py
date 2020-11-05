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

    def ok(self):
        if self.success:
            return self.data
        else:
            raise ResultException(self)

    def __bool__(self):
        return self.success


def get_result_maker(success):
    def result_maker(msg="", data=None) -> Result:
        return Result(msg=msg, success=success, data=data)

    return result_maker


Success = get_result_maker(True)
Fail = get_result_maker(False)
RaiseFail = lambda msg="", data=None: Fail(msg, data).as_response()


class ResultException(Exception):
    def __init__(self, result):
        super().__init__()
        self.result = result


def return_result():
    def wrapper(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs) -> Result:
            try:
                res = fn(*args, **kwargs)
                return res if isinstance(res, Result) else Success(data=res)
            except ResultException as e:
                return e.result

        return wrapped

    return wrapper


def method_wrapper(router_method):
    @wraps(router_method)
    def method_wrapped(*args, **kwargs):
        def wrapper(endpoint):
            @wraps(endpoint)
            async def wrapped(*args, **kwargs):
                try:
                    res = await endpoint(*args, **kwargs)
                    return res.as_response() if isinstance(res, Result) else res
                except ResultException as e:
                    return e.result.as_response()

            return router_method(*args, **kwargs)(wrapped)

        return wrapper

    return method_wrapped


def ResultAPIRouter():
    from fastapi import APIRouter

    router = APIRouter()
    router.get = method_wrapper(router.get)
    router.post = method_wrapper(router.post)
    router.put = method_wrapper(router.put)
    router.delete = method_wrapper(router.delete)
    return router
