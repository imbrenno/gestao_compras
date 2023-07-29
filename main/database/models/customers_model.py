from typing import Optional
from sqlmodel import Field, SQLModel



class Customers(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    companyName: str = Field(unique=True)
    tradingName: Optional[str] = Field(unique=True)
    vat: str = Field(max_length=14, min_length=14, unique=True)
    representative: Optional[str] = None
    contact: Optional[str] = None
    address: Optional[str] = None
    active: Optional[bool] = True
    walletManagerId: Optional[int] = Field(default=None, foreign_key="users.id")