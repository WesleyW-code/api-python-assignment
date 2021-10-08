from sqlalchemy.orm import Session
from app.api import models, schemas

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

def get_patient_by_name(db: Session, name: str):
    return db.query(models.Patient).filter(models.Patient.name == name).first()

def get_patient_by_id(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    
def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Patient).offset(skip).limit(limit).all()
    

def create_patient(db: Session, patient: schemas.PatientCreate, contact_num):
    db_patient = models.Patient(name=patient.name,contact_number=contact_num)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: int):
    db.query(models.Patient).filter(models.Patient.id == patient_id).delete()
    db.commit()
    return {"message": "Patient deleted"}


# def get_appointments(db: Session, skip: int = 0, limit: int = 100):

def create_patient_appointment(db: Session, appointment: schemas.AppointmentCreate, patient_id: int):
    db_appt = models.Appointment()
    db.add(db_appt)
    db.commit()
    db.refresh(db_appt)
    return db_appt


# def get_appointment_by_id(db: Session, appointment_id: int):

# def delete_patient_appointment(db: Session, appointment_id: int):
