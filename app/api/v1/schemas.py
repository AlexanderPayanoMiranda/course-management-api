from pydantic import BaseModel, constr


class CourseBase(BaseModel):
    subject: str
    courseNumber: constr(pattern=r"^\d{3}$")  # Ensures three-digit number
    description: str


class CourseCreate(CourseBase):
    pass


class Course(CourseBase):
    id: int

    class Config:
        from_attributes = True  # This replaces the old `orm_mode`
