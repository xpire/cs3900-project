"""
System for error and response handling internally and for API responses.

The system is inspried from the Or_error.t monad from OCaml and the Error monad from Haskell, 
but implemented in a Pythonic way.
"""

from functools import wraps
from typing import Any, Optional

from pydantic import BaseModel as BaseSchema
from src.core.utilities import HTTP400, log_msg


class Response(BaseSchema):
    """Generic API response type"""

    msg: str


class Result(BaseSchema):
    """Generic internal return type"""

    msg: str = ""
    success: bool
    data: Optional[Any]

    def log(self, log_level=None):
        """
        Record the contained message to the logging system
        """
        if self.success:
            log_level = log_level or "INFO"
        else:
            log_level = log_level or "ERROR"

        log_msg(self.msg, log_level)
        return self

    def as_response(self):
        """
        Convert [self] to an API response (a message or an exception)
        """
        if self.success:
            return Response(msg=self.msg)
        else:
            raise HTTP400(self.msg)

    def ok(self):
        """
        Return data if successful otherwise raise
        """
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
    """
    An exception that can be used to short circuit through blocks of code, as explained
    in [result_result()] and [ResultAPIRouter]

    This allows for clean syntax in code.
    """

    def __init__(self, result):
        super().__init__()
        self.result = result


def return_result():
    """
    Allows short circuiting of results - catches ResultException and converts it back into a
    failure [Result] instance. See [ResultAPIRouter] for how it is exactly used and its effects.
    """

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
    """
    Given a router method (e.g. router.get) this modifies the method such that the routed endpoint functions
    are automatically decorated by return_result(). See [ResultAPIRouter] for how it is exactly used and its effects.

    Args:
        router_method: HTTP router method (get/post/delete etc.)
    """

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
    """
    Returns fastAPI's APIRouter, but its methods are patched so that they are
    automatically decorated with [return_result()].

    This allows coding like following:

    ```
    @router.delete("")
    async def delete_watchlist(
        symbol: str = Depends(check_symbol),
        user_m: models.user = Depends(get_current_user_m),
        db: Session = Depends(get_db),
    ) -> Result:
        crud.user.delete_from_watchlist(symbol=symbol, db=db, user=user_m).ok()
        return Success(f"{symbol} removed from watchlist")
    ```

    The above endpoint calls .ok() on the result of crud operation. If the result was
    a failure, then it would raise a ResultException, but because @router.delete("")
    automatically wraps the endpoint function in [@return_result()], this exception
    would be safely caught and converted into an error message (i.e. HTTP400 exception with
    its error message corresponding to that contained in the failure result)
    """
    from fastapi import APIRouter

    router = APIRouter()
    router.get = method_wrapper(router.get)
    router.post = method_wrapper(router.post)
    router.put = method_wrapper(router.put)
    router.delete = method_wrapper(router.delete)
    return router
