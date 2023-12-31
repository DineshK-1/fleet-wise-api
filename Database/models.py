from .sql import Base
from sqlalchemy import DATE, TIMESTAMP, Column, Integer, String, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

class Cab(Base):
    __tablename__ = "cabs"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    cab_model = Column(String(100), nullable=False)
    cab_color = Column(String(40), nullable=False)
    cab_regno = Column(String(50), nullable=False)

    created_date = Column(DATE, nullable=False, server_default=func.now())
    time_updated = Column(TIMESTAMP(timezone=True), onupdate=func.now())

    driver_id = Column(Integer, ForeignKey('drivers.id', ondelete='SET NULL'), unique=True)
    driver = relationship('Driver', back_populates='cab')

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

    cab = relationship('Cab', back_populates='driver', uselist=False, cascade='all, delete-orphan')