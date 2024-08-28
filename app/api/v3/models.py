from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base
from .database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String(10), index=True)
    courseNumber = Column(String(3), index=True)
    description = Column(String, index=True)
    credits = Column(Integer, nullable=True)
    instructor = Column(String(100), nullable=True)
    semester = Column(String(10), nullable=True)
    capacity = Column(Integer, nullable=True)
