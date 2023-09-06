from typing import Optional
from sqlmodel import Field, SQLModel
from main.database.models.users_model import Users
from main.utils.enums.supplier import SuplierPaymentTypesEnum


class Suppliers(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    companyName: str = Field(unique=True)
    tradingName: Optional[str] = Field(unique=True)
    vat: str = Field(max_length=14, min_length=14, unique=True)
    representative: Optional[str] = None
    contact: Optional[str] = Field(max_length=1000, default=None)
    address: Optional[str] = Field(max_length=1000, default=None)
    category: Optional[str] = None
    paymentTypes: Optional[SuplierPaymentTypesEnum] = None
    active: Optional[bool] = True
    walletManagerId: Optional[int] = Field(default=None, foreign_key=Users.id)
