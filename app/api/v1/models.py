from sqlalchemy import Column, Integer, String
from .database import Base


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, index=True)
    courseNumber = Column(String(3), index=True)
    description = Column(String, index=True)
