from pydantic import BaseModel, constr
from typing import ClassVar


class CourseBase(BaseModel):
    subject: str
    courseNumber: constr(pattern=r"^\d{3}$")
    description: str
    ConfigDict: ClassVar = {"from_attributes": True}


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseBase):
    pass


class Course(CourseBase):
    id: int

    class Config:
        from_attributes = True
