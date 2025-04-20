from pydantic import BaseModel, validator
from typing import Optional

class UserBase(BaseModel):
    username: str
    last_name: str

class Users(UserBase):
    first_name: str
    age:int
    premium: bool
    height: int
    weight: int

    @validator('age')
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Age must be positive')
        return v
    
    @validator('first_name', 'last_name')
    def name_must_contain_letters(cls, v):
        if not v.isalpha():
            raise ValueError('Must contain only letters')
        return v.title()

class UpdateUser(BaseModel):
    first_name: Optional[str] = None
    age: Optional[str] = None

