from sqlalchemy.orm import Session
from app.api import models, schemas
import datetime

### These are all my crud operations! ###

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
# Notes:
# db refers to the current SQL session.
# models.X refers to the SQL table called X when called in a query
# models.X refers to the class X in the models.py (When not in a query)
# models.X.Y refers to column Y of SQL table called X (Example: models.Patient.id / refers to the id column in the patients SQL table.)
# .first() - returns the first row of data requested.
# .all() - returns all the rows of data requested.
# .delete() - deletes all rows of data requested.
# .update(X) - updates data requested with X (X is a dictionary)
#---------------------------------------------------------------------------------------------------------------------------------------------------------------

### My information fetching opperations: ###

# Find a patient by patient id.
def get_patient(db: Session, patient_id: int): 
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

# Find a patient by patient name.
def get_patient_by_name(db: Session, name: str):
    return db.query(models.Patient).filter(models.Patient.name == name).first()

# Find a patient by patient id. (duplicate but too scared to delete haha!)
def get_patient_by_id(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

# Retrieve all patients.  
def get_patients(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Patient).offset(skip).limit(limit).all()

# Find appointments for a specific patient.
def get_appointment_by_id(db: Session, patient_id: int):
    return db.query(models.Appointment).filter(models.Appointment.patient_id == patient_id).all()

# Find appointment with specific appointment id.
def get_appointment_by_appt_id(db: Session, id: int):
    return db.query(models.Appointment).filter(models.Appointment.id == id).first()

# Retrieve all apointments.
def get_appointments(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Appointment).offset(skip).limit(limit).all()

#---------------------------------------------------------------------------------------------------------------------------------------------------------------
### My creating and deleting operations: ###

# Function to add a new patient.

def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(name=patient.name,contact_number=patient.contact_number)
    # This adds the row to the database
    db.add(db_patient)
    # This saves the database with the new row added
    db.commit()
    # This is refreshing our information to include the id and appointments 
    # SO it adds the relationships and auto incremented columns
    db.refresh(db_patient)
    return db_patient

# Function to delete a patient by the patient id.

def delete_patient(db: Session, patient_id: int):
    db.query(models.Patient).filter(models.Patient.id == patient_id).delete()
    db.commit()
    return {"message": "Patient deleted"}

# Function to delete a appointment by the appointment id.

def delete_appointment(db: Session, id: int):
    db.query(models.Appointment).filter(models.Appointment.id == id).delete()
    db.commit()
    return {"message": "Appointment deleted"}

# Function to delete all appointments for a specific patient.

def delete_appointments_by_patient_id(db: Session, patient_id: int):
    db.query(models.Appointment).filter(models.Appointment.patient_id == patient_id).delete()
    db.commit()
    return {"message": "All appointments deleted for this patient"}

# Function to create an appointment for a specific patient.

def create_patient_appointment(db: Session, appointment: schemas.AppointmentCreate, patient_id: int):
    str_date = appointment.yyyy_mm_dd +" "+appointment.time
    time_input = datetime.datetime.strptime(str_date,'%Y/%m/%d %H:%M')

    # Checking if any times overlap and giving error if so.
    check = True
    # Getting all the appointments into a list to check each one for an overlap
    all_appointments = get_appointments(db)
    for appt in all_appointments:
        # Converting the String date from the database to a Datetime object!
        time_conv = datetime.datetime.strptime(appt.appt_time,'%Y-%m-%d %H:%M:%S')
        # This is the diffrence between the new appointment time and a current appointment in the database.
        difference = time_input - time_conv
        difference = difference.total_seconds()
        mins = difference/60
        
        # This checks that new appointment doesnt start at the same time as a current appointment.
        if mins ==0:
            check=False

        # This checks that new appointment doesn't start during a current appointment
        elif mins < appt.appt_length and mins > 0:
            check=False

        # This checks that new appointment doesn't end during a current appointment 
        elif mins > -appointment.appt_length and mins < 0:
            check=False
            
    # If check is false then the new appointment overlaps with a current one.
    if check == False:
        return None

    else:
        db_appt = models.Appointment(patient_id = patient_id, appt_length =appointment.appt_length, appt_time = time_input)
        db.add(db_appt)
        db.commit()
        db.refresh(db_appt)
        return db_appt

# Update a patient operation.

def update_patient(db: Session, patient_id: int, patient: schemas.PatientCreate):
    db.query(models.Patient).filter(models.Patient.id == patient_id).update(patient)
    db.commit()
    return get_patient_by_id(db=db ,patient_id=patient_id)

# Update a appointment operation.

def update_appointment(db: Session, patient_id: int, id: int, appointment: schemas.AppointmentCreate):
    str_date = appointment.yyyy_mm_dd +" "+appointment.time
    time_input = datetime.datetime.strptime(str_date,'%Y/%m/%d %H:%M')

    # Checking if any times overlap and giving error if so.
    check = True
    # Getting all appointments that are not the appointment we want to change.
    all_appointments = db.query(models.Appointment).filter(models.Appointment.id != id).all()

    # Going through each appointment and looking for overlap (similar to create appointment)
    for appt in all_appointments:
        time_conv = datetime.datetime.strptime(appt.appt_time,'%Y-%m-%d %H:%M:%S')
        difference = time_input - time_conv
        difference = difference.total_seconds()
        mins = difference/60
        
        # This checks that new appointment doesnt start at the same time as a current appointment.
        if mins ==0:
            check=False

        # This checks that new appointment doesn't start during a current appointment
        elif mins < appt.appt_length and mins > 0:
            check=False

        # This checks that new appointment doesn't end during a current appointment 
        elif mins > -appointment.appt_length and mins < 0:
            check=False

    if check == False:
        return None

    else:
        db_appt = dict(patient_id = patient_id, appt_length =appointment.appt_length, appt_time = time_input)
        db.query(models.Appointment).filter(models.Appointment.id == id).update(db_appt)
        db.commit()
        return get_appointment_by_appt_id(db, id=id)   






