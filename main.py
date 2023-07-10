from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session, joinedload
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func, update

from Database import models
from Database.sql import engine, SessionLocal
from Database.schema import CabBase, CabsResponse, DriversResponse, DriverBase, DeleteResponse, SearchRequest

from Database.validation import validateDriver, validateCab, validateEmail

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
    return {"cabs" : db.query(models.Cab).order_by(models.Cab.id).all()}

@app.post("/create_cab", tags=["Cabs"], response_model=CabBase)
def create_cab(model: str, color: str, regno: str, db: Session = Depends(get_db)):
    validation = validateCab(model, color, regno)
    if validation == True:
        cab_object = models.Cab(cab_model = model, cab_color=color, cab_regno = regno)

        try:
            db.add(cab_object)
            db.commit()
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Error creating cab")
        
        return cab_object
    else:
        raise HTTPException(status_code=422, detail=validation) 
    
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
    
@app.post("/delete_cab", response_model=DeleteResponse, tags=["Cabs"])
def delete_cab(id: int, db: Session = Depends(get_db)):
    cab = db.query(models.Cab).filter(models.Cab.id == id).first()

    if not cab:
        raise HTTPException(status_code=404, detail="Driver not found")
    try:
        db.delete(cab)
        db.commit()

        return {"deleted":True}
    except:
        raise HTTPException(status_code=404, detail="Error deleting Cab")
    
@app.get("/get_drivers", response_model = DriversResponse, tags=["Drivers"])
def get_drivers(db: Session = Depends(get_db)):
    query = db.query(models.Driver).options(joinedload(models.Driver.cab)).order_by(models.Driver.driver_ID).all()

    return {"drivers" : query}

@app.post("/get_drivers", response_model = DriversResponse, tags=["Drivers"])
def query_drivers(data: SearchRequest, db: Session = Depends(get_db)):
    query = db.query(models.Driver)

    if data.name:
        query = query.filter(func.concat(models.Driver.driver_first_name+ " " + models.Driver.driver_last_name).ilike(f"%{data.name}%"))
    if data.ID:
        query = query.filter(models.Driver.driver_ID == data.ID)
        
    query = query.order_by(models.Driver.driver_ID).all()
    return {"drivers" : query}
    
@app.post("/create_driver", tags=["Drivers"], response_model=DriverBase)
def create_driver(first_name: str, last_name: str, ID: int, email: str, phone: int, db: Session = Depends(get_db)):
    validation = validateDriver(first_name, last_name, ID, phone, email)

    if validation == True:
        driver_object = models.Driver(driver_first_name=first_name, driver_last_name=last_name, driver_ID = ID, driver_email = email, driver_phone=phone)

        try:
            db.add(driver_object)
            db.commit()
        except SQLAlchemyError:
            raise HTTPException(status_code=500, detail="Error creating driver")
        
        return driver_object
    else:
        raise HTTPException(status_code=422, detail=validation)
    
@app.put("/update_driver", response_model = DriverBase, tags=["Drivers"])
def update_driver(id: int, first_name: str = None, last_name: str = None, ID: int = None, email: str = None, phone: int = None, db: Session = Depends(get_db)):
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
            if not validateEmail(email):
                raise HTTPException(status_code=500, detail="Enter a valid email address")
            driver_object.driver_email = email
        if phone:
            driver_object.driver_phone = phone

        db.commit()

        return driver_object
    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Error updating Driver")
    
@app.post("/delete_driver", response_model=DeleteResponse, tags=["Drivers"])
def delete_driver(id: int, db: Session = Depends(get_db)):
    driver = db.query(models.Driver).filter(models.Driver.id == id).first()

    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    try:
        db.delete(driver)
        db.commit()

        return {"deleted":True}
    except:
        raise HTTPException(status_code=404, detail="Error deleting driver")
    
@app.post("/assign_cab", response_model=CabBase, tags=["Cabs"])
def assign_cab(cab_id: int, driver_id: int, db: Session = Depends(get_db)):
    cab = db.query(models.Cab).filter(models.Cab.id == cab_id).first()
    driver = db.query(models.Driver).filter(models.Driver.id == driver_id).first()

    if not cab:
        raise HTTPException(status_code=404, detail="Cab not found")
    if not driver:
        raise HTTPException(status_code=404, detail="Driver not found")
    
    cab.driver_id = driver.id
    try:
        db.commit()
    except:
        raise HTTPException(status_code=404, detail="Error assigning cab")
    
    cab = db.query(models.Cab).filter(models.Cab.id == cab_id).first()
    return cab

@app.post("/delete_cab_assignment", response_model=CabBase, tags=["Cabs"])
def delete_cab_assignment(cab_id: int, db: Session = Depends(get_db)):
    cab = db.query(models.Cab).filter(models.Cab.id == cab_id).first()
    if not cab:
        raise HTTPException(status_code=404, detail="Cab not found")
    if not cab.driver:
        raise HTTPException(status_code=404, detail="Cab has no driver assigned")
    
    cab.driver_id = None

    try:
        db.commit() 
    except:
        raise HTTPException(status_code=404, detail="Error assigning cab")
    
    db.refresh(cab)
    return cab