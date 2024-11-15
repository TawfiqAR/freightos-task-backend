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

@router.get("/generate")
def generate(db: Session = Depends(get_db)):
    generate_aggregated_market_rates(db)


@router.get("/calculate_savings/")
def calculate_savings(db: Session = Depends(get_db)):
    # Fetch Aggregated Market Rates from Database
    aggregated_data = db.execute(select(AggregatedMarketRateModel)).scalars().all()

    # Fetch User Rates from Database
    user_rates = db.execute(select(UserRateModel)).scalars().all()

    results = []

    # Iterate over user rates and find matching market data
    for user_rate in user_rates:
        # Find the market data that matches the same origin and destination
        matching_market_data = [
            market for market in aggregated_data
            if market.origin == user_rate.origin and market.destination == user_rate.destination
        ]

        if matching_market_data:
            market = matching_market_data[0]  # Assuming single match
            savings = {}

            # Calculate savings for each price percentile
            for price_type in ['min_price', 'percentile_10_price', 'median_price', 'percentile_90_price']:
                market_price = getattr(market, price_type)
                potential_savings = (market_price - user_rate.price) * user_rate.annual_volume if user_rate.annual_volume else Decimal(0)
                savings[f"potential_savings_{price_type}"] = f"${potential_savings:,.2f}"

            # Add the result
            results.append({
                "date": market.date.strftime('%Y-%m-%d'),
                "origin": user_rate.origin,
                "destination": user_rate.destination,
                "user_price": f"${user_rate.price:,.2f}",
                "min_price": f"${market.min_price:,.2f}",
                "percentile_10_price": f"${market.percentile_10_price:,.2f}",
                "median_price": f"${market.median_price:,.2f}",
                "percentile_90_price": f"${market.percentile_90_price:,.2f}",
                **savings  # Add the calculated savings to the result
            })

    return results