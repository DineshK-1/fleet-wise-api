
from datetime import date, datetime
from pydantic import BaseModel
from typing import Optional, List

class DriverForCabs(BaseModel):
    id: Optional[int]
    driver_first_name: Optional[str]
    driver_last_name: Optional[str]
    driver_ID: Optional[int]

    class Config:
        orm_mode = True

class CabBase(BaseModel):
    id: int
    cab_model: str
    cab_color: str
    cab_regno: str
    created_date: date
    time_updated: Optional[datetime]
    driver: Optional[DriverForCabs]

    class Config:
        orm_mode = True

class CabsResponse(BaseModel):
    cabs: List[CabBase]

class CabsForDrivers(BaseModel):
    id: Optional[int]
    cab_model: Optional[str]

    class Config:
        orm_mode = True

class DriverBase(BaseModel):
    id: int
    driver_first_name: str
    driver_last_name: str
    driver_ID: int
    driver_email: str
    driver_phone: int

    created_date: date
    time_updated: Optional[datetime]
    cab: Optional[CabsForDrivers]

    class Config:
        orm_mode = True

class DriversResponse(BaseModel):
    drivers: List[DriverBase]

class DeleteResponse(BaseModel):
    deleted: bool

class SearchRequest(BaseModel):
    name: Optional[str]
    ID: Optional[int]
    regno: Optional[str]
    model: Optional[str]
