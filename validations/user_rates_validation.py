from fastapi import UploadFile, File, Depends
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Any, Optional
from decimal import Decimal
from sqlmodel import SQLModel

def validate_and_convert_date(date_str: Any) -> Optional[datetime]:
    """
    Validates and converts a date string into a datetime object.
    Returns None if the input is invalid or not a string.
    """
    if not isinstance(date_str, str):
        return None
    try:
        return datetime.strptime(date_str, '%m/%d/%Y')
    except ValueError:
        return None

def preprocess_data(data: dict) -> dict:
    """
    Preprocesses the data to convert date strings to datetime objects.
    """
    if "effective_date" in data:
        data["effective_date"] = validate_and_convert_date(data["effective_date"])
    if "expiry_date" in data:
        data["expiry_date"] = validate_and_convert_date(data["expiry_date"])
    return data