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


@router.post(
    "/courses/batch/",
    response_model=list[schemas.Course],
    status_code=status.HTTP_201_CREATED,
)
def create_courses(courses: list[schemas.CourseCreate], db: Session = Depends(get_db)):
    duplicates = []

    for course in courses:
        existing_course = crud.get_course_by_subject_and_number(
            db, subject=course.subject, courseNumber=course.courseNumber
        )
        if existing_course:
            duplicates.append(course)

    if duplicates:
        raise HTTPException(
            status_code=400,
            detail=f"Duplicate courses found: {[f'{course.subject} {course.courseNumber}' for course in duplicates]}",
        )

    return crud.create_courses(db=db, courses=courses)


@router.get("/courses/", response_model=list[schemas.Course])
def get_courses(
    subject: str = Query(None),
    courseNumber: str = Query(None),
    instructor: str = Query(None),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
):
    filters = {}
    if subject:
        filters["subject"] = subject
    if courseNumber:
        filters["courseNumber"] = courseNumber
    if instructor:
        filters["instructor"] = instructor

    courses = crud.get_courses(db, skip=skip, limit=limit, filters=filters)
    if not courses:
        raise HTTPException(status_code=404, detail="Courses not found")
    return courses


@router.get("/courses/{course_id}", response_model=schemas.Course)
def get_course(course_id: int, db: Session = Depends(get_db)):
    db_course = crud.get_course_by_id(db, course_id=course_id)
    if db_course is None:
        raise HTTPException(status_code=404, detail="Course not found")
    return db_course


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


@router.delete("/courses/batch/")
def delete_multiple_courses(course_ids: dict, db: Session = Depends(get_db)):
    ids = course_ids.get("course_ids", [])
    deleted_courses = crud.delete_multiple_courses(db=db, course_ids=ids)
    if not deleted_courses:
        raise HTTPException(status_code=404, detail="No courses found to delete")
    return {"deleted_courses": deleted_courses}
