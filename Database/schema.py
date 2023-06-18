
from datetime import date, datetime
from pydantic import BaseModel


class CabBase(BaseModel):
    id: int
    cab_name: str
    cab_model: str
    cab_color: str
    cab_regno: str
    created_date: date
    time_updated: datetime

    class Config:
        orm_mode = True