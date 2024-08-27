from fastapi import APIRouter, HTTPException, Depends, Query, status
from sqlalchemy.orm import Session
from . import crud, schemas, models
from .database import get_db

router = APIRouter()


@router.post(
    "/courses/", response_model=schemas.Course, status_code=status.HTTP_201_CREATED
)
def create_course(course: schemas.CourseCreate, db: Session = Depends(get_db)):
    db_course = crud.get_course_by_subject_and_number(
        db, subject=course.subject, courseNumber=course.courseNumber
    )
    if db_course:
        raise HTTPException(status_code=400, detail="Course already exists")
    return crud.create_course(db=db, course=course)


@router.get("/courses/", response_model=list[schemas.Course])
def get_courses(
    description: str = Query(None),
    subject: str = Query(None),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    if description:
        courses = crud.get_courses_by_description_and_subject(
            db, description=description, subject=subject
        )
    else:
        courses = crud.get_courses(db, skip=skip, limit=limit)
    if not courses:
        raise HTTPException(status_code=404, detail="Courses not found")
    return courses


@router.put("/courses/{course_id}", response_model=schemas.Course)
def update_course(
    course_id: int,
    course: schemas.CourseUpdate,
    db: Session = Depends(get_db),
):
    db_course = crud.get_course_by_id(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud.update_course(db=db, course=course, course_id=course_id)


@router.delete("/courses/{course_id}", response_model=schemas.Course)
def delete_course(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course_by_id(db, course_id=course_id)
    if not db_course:
        raise HTTPException(status_code=404, detail="Course not found")
    return crud.delete_course(db=db, course_id=course_id)
