from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import date


# ---------- Class ----------
class ClassBase(BaseModel):
    name: str
    section: Optional[str] = None


class ClassCreate(ClassBase):
    pass


class ClassOut(ClassBase):
    id: int
    class Config:
        from_attributes = True


# ---------- Teacher ----------
class TeacherBase(BaseModel):
    name: str
    subject: Optional[str] = None
    email: EmailStr
    phone: Optional[str] = None


class TeacherCreate(TeacherBase):
    pass


class TeacherOut(TeacherBase):
    id: int
    class Config:
        from_attributes = True


# ---------- Student ----------
class StudentBase(BaseModel):
    name: str
    roll_number: str
    date_of_birth: Optional[date] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    class_id: Optional[int] = None


class StudentCreate(StudentBase):
    pass


class StudentOut(StudentBase):
    id: int
    class Config:
        from_attributes = True


# ---------- Attendance ----------
class AttendanceBase(BaseModel):
    student_id: int
    date: date
    status: str  # present / absent / leave


class AttendanceCreate(AttendanceBase):
    pass


class AttendanceOut(AttendanceBase):
    id: int
    class Config:
        from_attributes = True
