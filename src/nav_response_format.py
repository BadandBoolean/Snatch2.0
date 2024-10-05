from pydantic import BaseModel
from typing import Literal, Union

class NavResponseFormat(BaseModel):
    action: Union[Literal["Proceed", "Report", "Kill"], None] = None
    method: Union[Literal["Click", "Navigate"], None] = None
    xpath: Union[str, None] = None
    attribute: Union[str, None] = None
    datetimes: Union[list[str], None] = None
    
    class Config:
        extra = "forbid"

