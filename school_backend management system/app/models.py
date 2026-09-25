from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from .database import Base


class SchoolClass(Base):
    __tablename__ = "classes"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)   # e.g. "Class 9-A"
    section = Column(String(20), nullable=True)

    students = relationship("Student", back_populates="school_class")


class Teacher(Base):
    __tablename__ = "teachers"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    subject = Column(String(100), nullable=True)
    email = Column(String(100), unique=True, nullable=False)
    phone = Column(String(20), nullable=True)


class Student(Base):
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    roll_number = Column(String(20), unique=True, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    email = Column(String(100), unique=True, nullable=True)
    phone = Column(String(20), nullable=True)
    class_id = Column(Integer, ForeignKey("classes.id"), nullable=True)

    school_class = relationship("SchoolClass", back_populates="students")
    attendances = relationship("Attendance", back_populates="student")


class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    date = Column(Date, nullable=False)
    status = Column(String(10), nullable=False)  # "present" / "absent" / "leave"

    student = relationship("Student", back_populates="attendances")
