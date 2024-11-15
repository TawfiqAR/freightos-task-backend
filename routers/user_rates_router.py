from fastapi import File, UploadFile, APIRouter

from cruds.user_rates_crud import create_user_rates
from models.user_rates_model import UserRateModel

from fastapi import Depends
from sqlalchemy.orm import Session

from configs.database import get_db
from utils.csv_util import convert_to_json
from validations.user_rates_validation import preprocess_data

router = APIRouter(
    prefix="/user_rates",
    tags=["user_rates"],
)

@router.post("/")
def upload(file: UploadFile = File(...), db: Session = Depends(get_db)):
    data = convert_to_json(file)
    for user_rate in data.values():
        processed_first = preprocess_data(user_rate)
        if processed_first.get("effective_date") is None or processed_first.get("expiry_date") is None:
            return {"error": "Invalid dates in the uploaded data"}
        entry = UserRateModel(**processed_first)
        create_user_rates(entry, db)
    return data