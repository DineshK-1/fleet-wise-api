from .sql import Base
from sqlalchemy import DATE, TIMESTAMP, Column, Integer, String
from sqlalchemy.sql import func

class Cab(Base):
    __tablename__ = "cabs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cab_model = Column(String(100), nullable=False)
    cab_color = Column(String(40), nullable=False)
    cab_regno = Column(String(50), nullable=False)

    created_date = Column(DATE, nullable=False, server_default=func.now())
    time_updated = Column(TIMESTAMP(timezone=True), onupdate=func.now())

class Driver(Base):
    __tablename__ = "drivers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    driver_first_name = Column(String(200), nullable=False)
    driver_last_name = Column(String(200), nullable=False)
    driver_ID = Column(Integer, nullable=False)
    driver_email = Column(String(200), nullable=False)
    driver_phone = Column(String(15), nullable=False)

    created_date = Column(DATE, nullable=False, server_default=func.now())
    time_updated = Column(TIMESTAMP(timezone=True), onupdate=func.now())