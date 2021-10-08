from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from app.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    contact_number = Column(String, unique=True, index=True)

    appointments = relationship("Appointment", back_populates="patient")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    #name = Column(String, unique=True, index=True)
    # date = Column(String,unique=True, index=True)
    #length = Column(Integer,primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"))


    patient = relationship("Patient", back_populates="appointments")