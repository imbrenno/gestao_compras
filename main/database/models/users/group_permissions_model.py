from typing import Optional
from sqlmodel import Field, SQLModel
from main.database.models.users.routes_model import Routes
from main.database.models.users.user_groups_model import UserGroups

class GroupPermissions(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    userGroupsId: Optional[int] =  Field(default=None, foreign_key=UserGroups.id)
    routeId: Optional[int] =  Field(default=None, foreign_key=Routes.id)
    
