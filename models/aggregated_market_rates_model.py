from datetime import datetime
from decimal import Decimal
from typing import Optional

from sqlmodel import Field, SQLModel


class AggregatedMarketRateModel(SQLModel, table=True):
    __tablename__ = "aggregated_market_rates"
    id: int = Field(default=None, primary_key=True)
    date: datetime = Field(index=True)
    origin: str = Field(index=True)
    destination: str = Field(index=True)
    min_price: Decimal = Field(default=None)
    percentile_10_price: Decimal = Field(default=None)
    median_price: Decimal = Field(default=None)
    percentile_90_price: Decimal = Field(default=None)