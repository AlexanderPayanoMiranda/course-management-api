from sqlalchemy.orm import Session
from . import models, schemas


def get_courses(db: Session, skip: int = 0, limit: int = 10, filters: dict = None):
    query = db.query(models.Course)
    if filters:
        if "subject" in filters:
            query = query.filter(models.Course.subject == filters["subject"])
        if "courseNumber" in filters:
            query = query.filter(models.Course.courseNumber == filters["courseNumber"])
        if "instructor" in filters:
            query = query.filter(models.Course.instructor == filters["instructor"])
        if "credits" in filters:
            query = query.filter(models.Course.credits == filters["credits"])
        if "semester" in filters:
            query = query.filter(models.Course.semester == filters["semester"])
        if "description" in filters:
            query = query.filter(
                models.Course.description.ilike(f"%{filters['description']}%")
            )
    return query.offset(skip).limit(limit).all()


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


def create_course(db: Session, course: schemas.CourseCreate):
    db_course = models.Course(
        subject=course.subject,
        courseNumber=course.courseNumber,
        description=course.description,
        credits=course.credits,
        instructor=course.instructor,
        semester=course.semester,
        capacity=course.capacity,
    )
    db.add(db_course)
    db.commit()
    db.refresh(db_course)
    return db_course


def create_courses(db: Session, courses: list[schemas.CourseCreate]):
    db_courses = [models.Course(**course.dict()) for course in courses]
    db.add_all(db_courses)
    db.commit()
    for db_course in db_courses:
        db.refresh(db_course)
    return db_courses


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


def delete_multiple_courses(db: Session, course_ids: list[int]):
    courses_to_delete = (
        db.query(models.Course).filter(models.Course.id.in_(course_ids)).all()
    )
    for db_course in courses_to_delete:
        db.delete(db_course)
    db.commit()
    return courses_to_delete
