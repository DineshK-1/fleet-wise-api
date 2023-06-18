from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from Database import models
from Database.sql import engine, SessionLocal

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

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

@app.get("/get_cabs")
def read(db: Session = Depends(get_db)):
    return db.query(models.Cab).all()

@app.post("/create_cab")
def create_cab(model: str, color: str, regno: str, db: Session = Depends(get_db)):
    cab_object = models.Cab(cab_model = model, cab_color=color, cab_regno = regno)
    db.add(cab_object)
    db.commit()
    print(cab_object)