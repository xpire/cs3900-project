from pydantic import Field

Const = lambda x: Field(x, const=x)
