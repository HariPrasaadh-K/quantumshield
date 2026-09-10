import datetime
from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class Roadmap(Base):
    __tablename__ = "roadmaps"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    planning_threat_horizon_years = Column(Integer, default=10)
    generated_at = Column(DateTime, default=datetime.datetime.utcnow)
    phases = Column(JSON, nullable=False)
    urgent_asset_count = Column(Integer, default=0)
    high_priority_count = Column(Integer, default=0)
    explanation = Column(Text, nullable=True)
    mosca_status = Column(String, default="PLANNED")
    required_security_window_years = Column(Integer, default=12)

    project = relationship("Project", back_populates="roadmaps")
