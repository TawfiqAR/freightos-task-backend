from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel


class UserRateModel(SQLModel, table=True):
    __tablename__ = "users_rates"
    id: int = Field(default=None, primary_key=True)
    user_email: Optional[str] = Field(default=None, index=True)
    origin: Optional[str] = Field(default=None, index=True)
    destination: Optional[str] = Field(default=None, index=True)
    effective_date: Optional[datetime] = Field(default=None, index=True)
    expiry_date: Optional[datetime] = Field(default=None, index=True)
    price: Optional[Decimal] = Field(default=None, index=True)
    annual_volume: Optional[Decimal] = Field(default=None, index=True)
