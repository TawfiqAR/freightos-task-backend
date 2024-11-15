import pandas as pd
import numpy as np
from sqlalchemy import text
from sqlalchemy.orm import Session

def generate_aggregated_market_rates(db: Session):
    try:
        query = "SELECT date, origin, destination, price FROM price_benchmark.market_rates"
        df = pd.read_sql(query, db.bind)

        aggregated_data = df.groupby(['date', 'origin', 'destination']).agg(
            min_price=('price', 'min'),
            percentile_10_price=('price', lambda x: np.percentile(x, 10)),
            median_price=('price', lambda x: np.percentile(x, 50)),
            percentile_90_price=('price', lambda x: np.percentile(x, 90))
        ).reset_index()
        with db.begin():
            db.execute(text("TRUNCATE TABLE price_benchmark.aggregated_market_rates"))
        aggregated_data.to_sql('aggregated_market_rates', con=db.bind, if_exists='append', index=False)
        db.commit()
        print("Aggregation successfully done")
    except Exception as e:
        print(f"An error occurred: {e}")