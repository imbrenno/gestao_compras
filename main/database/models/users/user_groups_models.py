from typing import Optional
from sqlmodel import Field, SQLModel


class UserGroups(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    GroupName: str
    routes: Optional[str]
