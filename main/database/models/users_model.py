from main.utils.enums.users import GenderEnum
from typing import Optional
from sqlmodel import Field, SQLModel


class Users(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user: str = Field(unique=True)
    password: str 
    fullName: str = Field(max_length=50, min_length=10)
    document: str = Field(max_length=14, min_length=11, unique=True)
    active: Optional[bool] = True
    gender: Optional[GenderEnum] = None
    
