import datetime
from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Project(Base):
    __tablename__ = "projects"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, nullable=False, index=True)
    source_type = Column(String, nullable=False) # zip, github, demo
    source_url = Column(String, nullable=True)
    status = Column(String, default="active") # active, archived
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    scans = relationship("Scan", back_populates="project", cascade="all, delete-orphan")
    roadmaps = relationship("Roadmap", back_populates="project", cascade="all, delete-orphan")
