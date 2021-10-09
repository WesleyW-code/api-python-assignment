from fastapi import Depends, FastAPI, HTTPException, Request, Response
from typing import List
from sqlalchemy.orm import Session
from app.api import crud, models, schemas
from app.database import SessionLocal, engine
from redis import Redis


from app.api import test
#---------------------------------------------------------------------------------------------------------------------------------------------------------------
# Notes:
# "Reponse_model=X" specifies that the output must be in the format X. This must correspond with the return statement for the funtion!

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

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

#---------------------------------------------------------------------------------------------------------------------------------------------------------------

### Patient and Appointment Operations ###

# To create a new patient into the SQL Database. (Can be tested on the http://localhost:8080/docs - this is where i do all my testing to see if it works.)
@app.post("/patient/", response_model=schemas.Patient)
def create_patients(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_patient = crud.get_patient_by_name(db, name=patient.name)
    if db_patient:
        raise HTTPException(status_code=400, detail="Patient already exists")
    return crud.create_patient(db=db, patient=patient)

# To show all the patients with their information.
@app.get("/patients/", response_model=List[schemas.Patient])
def read_patients(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    all_patients = crud.get_patients(db, skip=skip, limit=limit)
    return all_patients

# view a specific patient
@app.get("/patients/{patient_id}", response_model=schemas.Patient)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

# To create an appointment for a patient.
@app.post("/appointment/", response_model=schemas.Appointment)
def create_appt(patient_id: int, appt: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    db_appointment = crud.create_patient_appointment(db=db, appointment=appt, patient_id=patient_id)
    if db_appointment is None:
        raise HTTPException(status_code=404, detail="Appointment time not valid!")
    return db_appointment


# To read all the appointments
@app.get("/appointments", response_model= List[schemas.Appointment])
def read_appointments(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    appts = crud.get_appointments(db, skip=skip, limit=limit)
    return appts

# Getting all appointments for specific patient.
@app.get("/patients/{patient_id}/appointments", response_model=List[schemas.Appointment])
def read_appts(patient_id: int, db: Session = Depends(get_db)):
    db_patient = crud.get_patient(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return crud.get_appointment_by_id(db=db, patient_id=patient_id)

# To delete a specific patient.
@app.delete("/patient/{patient_id}", status_code=200)
def delete_patient(patient_id:int, db: Session = Depends(get_db)):
    db_patient = crud.get_patient_by_id(db, patient_id=patient_id)
    if db_patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return crud.delete_patient(db=db, patient_id=patient_id)

# To delete a specific appointment.
@app.delete("/appointment/{id}", status_code=200)
def delete_appointment(id:int, db: Session = Depends(get_db)):
    db_appt = crud.get_appointment_by_appt_id(db, id=id)
    if db_appt is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return crud.delete_appointment(db=db, id=id)

# To delete all the appointments of a patient(Something extra i added).
@app.delete("/patient/{patient_id}/delete", status_code=200)
def delete_all_for_patient(patient_id:int, db: Session = Depends(get_db)):
    db_appt = crud.get_appointment_by_id(db, patient_id = patient_id)
    if db_appt is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return crud.delete_appointments_by_patient_id(db=db, patient_id=patient_id)

# To edit a specific appointment.
# Response model is the format you want it to output in the end.
@app.put("/appointment/{id}/update", response_model=schemas.Appointment)
def edit_appointment (patient_id: int, id: int ,appt: schemas.AppointmentCreate, db: Session = Depends(get_db)):

    # Checking if the appointment exists.
    db_appt_exists = crud.get_appointment_by_appt_id(db, id=id)
    if db_appt_exists is None:
        raise HTTPException(status_code=404, detail="Appointment not found!")
    
    # Checking if the updated appointment time is valid.
    db_appt_updated = crud.update_appointment(db, patient_id=patient_id, id=id, appointment=appt)
    if db_appt_updated is None:
        raise HTTPException(status_code=404, detail="Appointment time not valid!")
    
    # Otherwise update the appointment.
    return db_appt_updated
    
# To edit a specific patient.
@app.put("/patient/{patient_id}/update", response_model=schemas.Patient)
def edit_patient(patient_id: int, patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    db_patient = crud.get_patient_by_id(db, patient_id=patient_id)

    # Break if the patient doesnt exist
    if db_patient is None:
        raise HTTPException(status_code=400, detail="Patient not found!")
    # Otherwise update the patient.
    return crud.update_patient(db=db, patient_id = patient_id, patient = patient) 