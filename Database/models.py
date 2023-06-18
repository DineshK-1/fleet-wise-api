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
