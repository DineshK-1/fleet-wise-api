
from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional, List


class CabBase(BaseModel):
    id: int
    cab_model: str
    cab_color: str
    cab_regno: str
    created_date: date
    time_updated: Optional[datetime]

    class Config:
        orm_mode = True

class CabsResponse(BaseModel):
    cabs: List[CabBase]

class DriverBase(BaseModel):
    id: int
    driver_first_name: str
    driver_last_name: str
    driver_ID: int
    driver_email: str
    driver_phone: int

    created_date: date
    time_updated: Optional[datetime]

    class Config:
        orm_mode = True

class DriversResponse(BaseModel):
    drivers: List[DriverBase]

class DeleteResponse(BaseModel):
    deleted: bool