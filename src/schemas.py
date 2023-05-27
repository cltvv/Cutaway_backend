from pydantic import BaseModel as PydanticBaseModel
from pydantic import root_validator
from datetime import datetime


class BaseModel(PydanticBaseModel):

    class Config:
        orm_mode = True