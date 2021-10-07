from fastapi import Depends, FastAPI, HTTPException, Request, Response
from typing import List
from sqlalchemy.orm import Session
from app.api import crud, models, schemas
from app.database import SessionLocal, engine
from redis import Redis


from app.api import test

# Uncomment the line below to let the ORM generate tables and relationships for us - if not using migrations
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    response = Response("Internal server error", status_code=500)
    try:
        request.state.db = SessionLocal()
        response = await call_next(request)
    finally:
        request.state.db.close()
    return response

# DB Dependency
def get_db(request: Request):
    return request.state.db

# health checker
@app.get("/health")
async def root():
    return {"message": "I am healthy"}

# health checker
@app.get("/test")
async def root():
    return test.testfunction()

# Basic crud operations
# @app.post("/appointment/", response_model=schemas.Brewer)

# @app.get("/appointments", response_model=List[schemas.Brewer])

# @app.get("/appointment/{id}", response_model=schemas.Recipe)

# @app.delete("/appointment/{id}", status_code=200)

# @app.put("/appointment/{id}", response_model=schemas.Brewer)

@app.post("/patients/", response_model=schemas.Patient)
def create_user(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_user = crud.get_patient_by_name(db, name=patient.name)
    if db_user:
        raise HTTPException(status_code=400, detail="Patient already exists")
    return crud.create_patient(db=db, patient=patient)
