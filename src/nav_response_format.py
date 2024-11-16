from pydantic import BaseModel
from typing import List, Optional, Union, Literal


class NavResponseFormat(BaseModel):
    why: str
    action: Literal["Proceed", "Report", "Kill"]
    selector: Literal["alt_text", "placeholder", "test_id", "text", "title", "xpath"]
    locator: str

    class Config:
        extra = "forbid"  # Disallow additional properties


class NavResponses(BaseModel):
    html: List[str] = None
    datetimes: List[str] = None

    class Config:
        extra = "forbid"  # Disallow additional properties
