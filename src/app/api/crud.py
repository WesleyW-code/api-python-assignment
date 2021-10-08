from sqlalchemy.orm import Session
from app.api import models, schemas
import datetime

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

def get_patient_by_name(db: Session, name: str):
    return db.query(models.Patient).filter(models.Patient.name == name).first()

def get_patient_by_id(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    
def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Patient).offset(skip).limit(limit).all()

    

def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(name=patient.name,contact_number=patient.contact_number)
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def delete_patient(db: Session, patient_id: int):
    db.query(models.Patient).filter(models.Patient.id == patient_id).delete()
    db.commit()
    return {"message": "Patient deleted"}

def delete_appointment(db: Session, id: int):
    db.query(models.Appointment).filter(models.Appointment.id == id).delete()
    db.commit()
    return {"message": "Appointment deleted"}

def delete_appointments_by_patient_id(db: Session, patient_id: int):
    db.query(models.Appointment).filter(models.Appointment.patient_id == patient_id).delete()
    db.commit()
    return {"message": "All appointments deleted for this patient"}


def get_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Appointment).offset(skip).limit(limit).all()


def create_patient_appointment(db: Session, appointment: schemas.AppointmentCreate, patient_id: int):
    str_date = appointment.yyyy_mm_dd +" "+appointment.time
    appt_time_constructor = datetime.datetime.strptime(str_date,'%Y/%m/%d %H:%M')
    db_appt = models.Appointment(patient_id = patient_id, appt_length =appointment.appt_length, appt_time = appt_time_constructor)
    db.add(db_appt)
    db.commit()
    db.refresh(db_appt)
    return db_appt


def get_appointment_by_id(db: Session, patient_id: int):
    return db.query(models.Appointment).filter(models.Appointment.patient_id == patient_id).all()

def get_appointment_by_appt_id(db: Session, id: int):
    return db.query(models.Appointment).filter(models.Appointment.id == id).first()
# def delete_patient_appointment(db: Session, appointment_id: int):
