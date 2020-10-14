from pydantic import BaseModel

class Msg(BaseModel):
    '''
    Return schema is always this
    '''
    msg: str
