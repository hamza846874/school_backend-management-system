from sqlalchemy.orm import Session
from . import models, schemas


# ---------- Class ----------
def create_class(db: Session, data: schemas.ClassCreate):
    obj = models.SchoolClass(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_classes(db: Session):
    return db.query(models.SchoolClass).all()


def get_class(db: Session, class_id: int):
    return db.query(models.SchoolClass).filter(models.SchoolClass.id == class_id).first()


def delete_class(db: Session, class_id: int):
    obj = get_class(db, class_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj


# ---------- Teacher ----------
def create_teacher(db: Session, data: schemas.TeacherCreate):
    obj = models.Teacher(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_teachers(db: Session):
    return db.query(models.Teacher).all()


def get_teacher(db: Session, teacher_id: int):
    return db.query(models.Teacher).filter(models.Teacher.id == teacher_id).first()


def delete_teacher(db: Session, teacher_id: int):
    obj = get_teacher(db, teacher_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj


# ---------- Student ----------
def create_student(db: Session, data: schemas.StudentCreate):
    obj = models.Student(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_students(db: Session):
    return db.query(models.Student).all()


def get_student(db: Session, student_id: int):
    return db.query(models.Student).filter(models.Student.id == student_id).first()


def update_student(db: Session, student_id: int, data: schemas.StudentCreate):
    obj = get_student(db, student_id)
    if obj:
        for key, value in data.dict().items():
            setattr(obj, key, value)
        db.commit()
        db.refresh(obj)
    return obj


def delete_student(db: Session, student_id: int):
    obj = get_student(db, student_id)
    if obj:
        db.delete(obj)
        db.commit()
    return obj


# ---------- Attendance ----------
def mark_attendance(db: Session, data: schemas.AttendanceCreate):
    obj = models.Attendance(**data.dict())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


def get_attendance_by_student(db: Session, student_id: int):
    return db.query(models.Attendance).filter(models.Attendance.student_id == student_id).all()
