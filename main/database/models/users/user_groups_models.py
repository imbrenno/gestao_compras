from typing import Optional
from sqlmodel import Field, SQLModel


class UserGroups(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    groupName: str
    active: Optional[bool] = True
