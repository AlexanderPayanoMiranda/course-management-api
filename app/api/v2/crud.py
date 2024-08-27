from sqlalchemy.orm import Session
from . import models, schemas


def get_course_by_id(db: Session, course_id: int):
    return db.query(models.Course).filter(models.Course.id == course_id).first()


def get_course_by_subject_and_number(db: Session, subject: str, courseNumber: str):
    return (
        db.query(models.Course)
        .filter(
            models.Course.subject == subject, models.Course.courseNumber == courseNumber
        )
        .first()
    )


def get_courses(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Course).offset(skip).limit(limit).all()


def get_courses_by_description_and_subject(
    db: Session, description: str, subject: str = None
):
    query = db.query(models.Course).filter(
        models.Course.description.ilike(f"%{description}%")
    )
    if subject:
        query = query.filter(models.Course.subject == subject)
    return query.all()


def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(
        subject=course.subject,
        courseNumber=course.courseNumber,
        description=course.description,
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def update_course(db: Session, course_id: int, course: schemas.CourseUpdate):
    db_course = get_course_by_id(db, course_id)
    if db_course is None:
        return None
    for key, value in course.dict(exclude_unset=True).items():
        setattr(db_course, key, value)
    db.commit()
    db.refresh(db_course)
    return db_course


def delete_course(db: Session, course_id: int):
    db_course = get_course_by_id(db, course_id)
    if db_course is None:
        return None
    db.delete(db_course)
    db.commit()
    return db_course
