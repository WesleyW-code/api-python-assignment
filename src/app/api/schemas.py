import datetime
from typing import List, Optional
from pydantic import BaseModel

class AppointmentBase(BaseModel):
    appt_length: int
    # description: Optional[str] = None
    # bean_type: Optional[str] = None
    # brew_time: Optional[float] = 0.0
    # brew_method: Optional[str] = None
    # taste_notes: Optional[str] = None
    # tags: Optional[str] = None

class AppointmentCreate(AppointmentBase):
    yyyy_mm_dd: str
    time: str

class Appointment(AppointmentBase):
    id: int
    patient_id: int
    appt_time: str

    class Config:
        orm_mode = True

class PatientBase(BaseModel):
    name: str
    contact_number: str

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    appointments: Optional[List[Appointment]] = []

    class Config:
        orm_mode = True
