from decimal import Decimal

from fastapi import APIRouter
from sqlalchemy import select

from cruds.aggregated_market_rates_crud import generate_aggregated_market_rates

from fastapi import Depends
from sqlalchemy.orm import Session

from configs.database import get_db
from models.aggregated_market_rates_model import AggregatedMarketRateModel
from models.user_rates_model import UserRateModel

router = APIRouter(
    prefix="/aggregated_market_rates",
    tags=["aggregated_market_rates"],
)

@router.get("/")
def get_all(db: Session = Depends(get_db)):
    result = db.execute(select(AggregatedMarketRateModel)).all()
    data = [dict(row._asdict()) for row in result]
    return data


@router.get("/generate")
def generate(db: Session = Depends(get_db)):
    generate_aggregated_market_rates(db)


@router.get("/calculate_savings/")
def calculate_savings(db: Session = Depends(get_db)):
    """
    Calculate the percentile savings by comparing user data to aggregated data
    """
    aggregated_data = db.execute(select(AggregatedMarketRateModel)).scalars().all()
    user_rates = db.execute(select(UserRateModel)).scalars().all()

    results = []

    for user_rate in user_rates:
        # Find all market data matching the same origin and destination
        matching_market_data = [
            market for market in aggregated_data
            if market.origin == user_rate.origin and market.destination == user_rate.destination
        ]

        # Process each matching market data
        for market in matching_market_data:
            savings = {}

            # Calculate savings for each price percentile
            for price_type in ['min_price', 'percentile_10_price', 'median_price', 'percentile_90_price']:
                market_price = getattr(market, price_type)
                potential_savings = (market_price - user_rate.price) * user_rate.annual_volume if user_rate.annual_volume else Decimal(0)
                savings[f"potential_savings_{price_type}"] = f"${potential_savings:,.2f}"

            # Append result for each market entry
            results.append({
                "date": market.date.strftime('%Y-%m-%d'),
                "origin": user_rate.origin,
                "destination": user_rate.destination,
                "user_price": f"${user_rate.price:,.2f}",
                "min_price": f"${market.min_price:,.2f}",
                "percentile_10_price": f"${market.percentile_10_price:,.2f}",
                "median_price": f"${market.median_price:,.2f}",
                "percentile_90_price": f"${market.percentile_90_price:,.2f}",
                **savings
            })

    return results