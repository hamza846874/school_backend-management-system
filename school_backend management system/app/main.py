from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud
from .database import engine, get_db
from .config import settings
from .auth import create_access_token, verify_admin, get_current_admin

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.APP_NAME, version="1.0.0")


@app.get("/")
def root():
    return {"message": f"{settings.APP_NAME} chal raha hai! /docs par jaa kar APIs dekhein."}


# ---------------- Auth ----------------
@app.post("/auth/login")
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    if not verify_admin(form_data.username, form_data.password):
        raise HTTPException(status_code=401, detail="Email ya password galat hai")
    token = create_access_token({"sub": form_data.username})
    return {"access_token": token, "token_type": "bearer"}


# ---------------- Classes ----------------
@app.post("/classes/", response_model=schemas.ClassOut)
def add_class(data: schemas.ClassCreate, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    return crud.create_class(db, data)


@app.get("/classes/", response_model=List[schemas.ClassOut])
def list_classes(db: Session = Depends(get_db)):
    return crud.get_classes(db)


@app.delete("/classes/{class_id}")
def remove_class(class_id: int, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    obj = crud.delete_class(db, class_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Class not found")
    return {"message": "Class deleted"}


# ---------------- Teachers ----------------
@app.post("/teachers/", response_model=schemas.TeacherOut)
def add_teacher(data: schemas.TeacherCreate, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    return crud.create_teacher(db, data)


@app.get("/teachers/", response_model=List[schemas.TeacherOut])
def list_teachers(db: Session = Depends(get_db)):
    return crud.get_teachers(db)


@app.delete("/teachers/{teacher_id}")
def remove_teacher(teacher_id: int, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    obj = crud.delete_teacher(db, teacher_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Teacher not found")
    return {"message": "Teacher deleted"}


# ---------------- Students ----------------
@app.post("/students/", response_model=schemas.StudentOut)
def add_student(data: schemas.StudentCreate, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    return crud.create_student(db, data)


@app.get("/students/", response_model=List[schemas.StudentOut])
def list_students(db: Session = Depends(get_db)):
    return crud.get_students(db)


@app.get("/students/{student_id}", response_model=schemas.StudentOut)
def get_one_student(student_id: int, db: Session = Depends(get_db)):
    obj = crud.get_student(db, student_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Student not found")
    return obj


@app.put("/students/{student_id}", response_model=schemas.StudentOut)
def edit_student(student_id: int, data: schemas.StudentCreate, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    obj = crud.update_student(db, student_id, data)
    if not obj:
        raise HTTPException(status_code=404, detail="Student not found")
    return obj


@app.delete("/students/{student_id}")
def remove_student(student_id: int, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    obj = crud.delete_student(db, student_id)
    if not obj:
        raise HTTPException(status_code=404, detail="Student not found")
    return {"message": "Student deleted"}


# ---------------- Attendance ----------------
@app.post("/attendance/", response_model=schemas.AttendanceOut)
def add_attendance(data: schemas.AttendanceCreate, db: Session = Depends(get_db), admin: str = Depends(get_current_admin)):
    return crud.mark_attendance(db, data)


@app.get("/attendance/{student_id}", response_model=List[schemas.AttendanceOut])
def student_attendance(student_id: int, db: Session = Depends(get_db)):
    return crud.get_attendance_by_student(db, student_id)
