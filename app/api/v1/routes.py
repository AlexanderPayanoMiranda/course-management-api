from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from . import crud, schemas
from .database import get_db

router = APIRouter()


@router.post("/courses/", response_model=schemas.Course)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = crud.get_course_by_subject_and_number(
        db, subject=course.subject, courseNumber=course.courseNumber
    )
    if db_course:
        raise HTTPException(status_code=400, detail="Course already exists")
    return crud.create_course(db=db, course=course)


@router.get("/courses/", response_model=List[schemas.Course])
def get_courses(description: str, db: Session = Depends(get_db)):
    courses = crud.get_courses_by_description(db, description=description)
    if not courses:
        raise HTTPException(status_code=404, detail="Courses not found")
    return courses


@router.delete("/courses/{course_id}", response_model=schemas.Course)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    return crud.delete_course(db, course_id)
