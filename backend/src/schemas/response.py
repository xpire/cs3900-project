from typing import Optional

from pydantic import BaseModel as BaseSchema


class Response(BaseSchema):
    msg: str
    value: Optional[int]