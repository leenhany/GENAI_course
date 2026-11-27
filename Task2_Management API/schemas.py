from pydantic import BaseModel,Field,ValidationError,field_validator
from typing import Optional,Literal

class TaskCreate(BaseModel):
   title: Optional[str]=Field(default=None,min_length=3,max_length=100)
   priotity:Literal['high','medium','low'] | None=None
   description:Optional[str]="No desciption"

   @field_validator("title")   
   @classmethod
   def validate_title(cls,value):
        if value and not value[0].isupper():
            raise ValueError("Title must start with uppercase.")
        return value

class TaskUpdate(BaseModel):
   title: Optional[str]=Field(default=None,min_length=3,max_length=10)
   priotity:Literal['high','medium','low'] | None=None
   description:Optional[str]

   @field_validator("title")   
   @classmethod
   def validate_title(cls,value):
        if value and not value[0].isupper():
            raise ValueError("Title must start with uppercase.")
        return value

class TakeResponse(BaseModel):
    task_id: int
    title: str
    priotity: Literal["low", "medium", "high"]
    description:str
    status: str
