from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError

from Database import models
from Database.sql import engine, SessionLocal
from Database.schema import CabBase, CabsResponse, DriversResponse, DriverBase

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Fleet Wise API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

@app.get("/get_cabs", response_model = CabsResponse, tags=["Cabs"])
def get_cabs(db: Session = Depends(get_db)):
    return {"cabs" : db.query(models.Cab).all()}

@app.post("/create_cab", tags=["Cabs"])
def create_cab(model: str, color: str, regno: str, db: Session = Depends(get_db)):
    cab_object = models.Cab(cab_model = model, cab_color=color, cab_regno = regno)

    try:
        db.add(cab_object)
        db.commit()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error creating cab")
    
@app.put("/update_cab", response_model = CabBase, tags=["Cabs"])
def update_cab(id: int, model: str = None, color: str = None, regno: str = None, db: Session = Depends(get_db)):
    try:
        cab_object = db.query(models.Cab).get(id)
        
        if cab_object == None:
            raise HTTPException(status_code=404, detail="Cab not found")

        if model:
            cab_object.cab_model = model
        if color:
            cab_object.cab_color = color
        if regno:
            cab_object.cab_regno = regno

        db.commit()

        return cab_object
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error updating cab")
    
@app.get("/get_drivers", response_model = DriversResponse, tags=["Drivers"])
def get_cabs(db: Session = Depends(get_db)):
    return {"drivers" : db.query(models.Driver).all()}
    
@app.post("/create_driver", tags=["Drivers"])
def create_driver(first_name: str, last_name: str, ID: int, email: str, phone: int, db: Session = Depends(get_db)):
    driver_object = models.Driver(driver_first_name=first_name, driver_last_name=last_name, driver_ID = ID, driver_email = email, driver_phone=phone)

    try:
        db.add(driver_object)
        db.commit()
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error creating driver")
    
@app.put("/update_driver", response_model = DriverBase, tags=["Drivers"])
def update_cab(id: int, first_name: str = None, last_name: str = None, ID: int = None, email: str = None, phone: int = None, db: Session = Depends(get_db)):
    try:
        driver_object = db.query(models.Driver).get(id)
        
        if driver_object == None:
            raise HTTPException(status_code=404, detail="Driver not found")

        if first_name:
            driver_object.driver_first_name = first_name
        if last_name:
            driver_object.driver_last_name = last_name
        if ID:
            driver_object.driver_ID = ID
        if email:
            driver_object.driver_email = email
        if phone:
            driver_object.driver_phone = phone

        db.commit()

        return driver_object
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error updating Driver")