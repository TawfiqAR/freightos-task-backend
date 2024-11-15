from fastapi import Depends
from sqlalchemy.orm import Session

from models.user_rates_model import UserRateModel
from configs.database import get_db

def create_user_rates(user_rate: UserRateModel , db: Session = Depends(get_db)):
    db.add(user_rate)
    db.commit()
    db.refresh(user_rate)
    return user_rate