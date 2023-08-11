from typing import Optional
from sqlmodel import Field, SQLModel


class Routes(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    routeName: str
    route: str
