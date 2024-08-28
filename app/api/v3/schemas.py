from pydantic import BaseModel, Field, validator, constr
from typing import Optional


class CourseBase(BaseModel):
    subject: str = Field(..., max_length=10)
    courseNumber: str = Field(..., pattern=r"^\d{3}$")
    description: str
    credits: Optional[int] = Field(None, ge=1, le=5)
    instructor: Optional[str] = Field(None, max_length=100)
    semester: Optional[constr(pattern=r"^(Fall|Spring|Summer) \d{4}$")] = Field(
        None, max_length=15
    )  # e.g., "Fall 2024"
    capacity: Optional[int] = Field(None, ge=1)

    class Config:
        from_attributes = True

    @validator("description")
    def validate_description(cls, v):
        if len(v) < 10:
            raise ValueError("Description must be at least 10 characters long.")
        return v

    @validator("capacity")
    def validate_capacity(cls, v):
        if v is not None and v < 5:
            raise ValueError("Capacity must be at least 5 if provided.")
        return v


class CourseCreate(CourseBase):
    pass


class CourseUpdate(CourseBase):
    subject: Optional[str] = Field(None, max_length=10)
    courseNumber: Optional[str] = Field(None, pattern=r"^\d{3}$")
    description: Optional[str]
    credits: Optional[int] = Field(None, ge=1, le=5)
    instructor: Optional[str] = Field(None, max_length=100)
    semester: Optional[constr(pattern=r"^(Fall|Spring|Summer) \d{4}$")] = Field(
        None, max_length=15
    )
    capacity: Optional[int] = Field(None, ge=1)

    class Config:
        from_attributes = True

    @validator("description", pre=True, always=True)
    def validate_description(cls, v):
        if v is not None and len(v) < 10:
            raise ValueError("Description must be at least 10 characters long.")
        return v

    @validator("capacity")
    def validate_capacity(cls, v):
        if v is not None and v < 5:
            raise ValueError("Capacity must be at least 5 if provided.")
        return v


class Course(CourseBase):
    id: int

    class Config:
        from_attributes = True
