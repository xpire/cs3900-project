from typing import Any, Optional

from pydantic import BaseModel as BaseSchema
from src.core.utilities import HTTP400, log_msg
from src.util.extended_types import Const


class Response(BaseSchema):
    msg: str


# Internal return type
class Result(BaseSchema):
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

    def __bool__(self):
        return self.success


class Success(Result):
    success = Const(True)


class Fail(Result):
    success = Const(False)
