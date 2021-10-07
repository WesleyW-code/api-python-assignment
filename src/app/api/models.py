from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import DateTime

from app.database import Base


class Patient(Base):
    __tablename__ = "patients"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    contact_number = Column(Integer, unique=True, index=True)

    appointment = relationship("Appointment", back_populates="patients")


class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, unique=True, index=True)
    date = Column(DateTime,unique=True, index=True)
    length = Column(Integer,primary_key=True, index=True)


    patient = relationship("Patient", back_populates="appointments")