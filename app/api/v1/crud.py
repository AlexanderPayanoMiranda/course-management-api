from sqlalchemy.orm import Session
from . import models, schemas


def get_course_by_subject_and_number(db: Session, subject: str, courseNumber: str):
    return (
        db.query(models.Course)
        .filter(
            models.Course.subject == subject, models.Course.courseNumber == courseNumber
        )
        .first()
    )


def get_courses_by_description(db: Session, description: str):
    # Use `ilike` for case-insensitive partial matching
    return (
        db.query(models.Course)
        .filter(models.Course.description.ilike(f"%{description}%"))
        .all()
    )


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


def delete_course(db: Session, course_id: int):
    db_course = db.query(models.Course).filter(models.Course.id == course_id).first()
    if db_course:
        db.delete(db_course)
        db.commit()
        return db_course
    return None
