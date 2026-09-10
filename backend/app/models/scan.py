import datetime
from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Scan(Base):
    __tablename__ = "scans"

    id = Column(String, primary_key=True, index=True)
    project_id = Column(String, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False)
    status = Column(String, default="pending") # pending, running, completed, failed
    started_at = Column(DateTime, default=datetime.datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    files_scanned = Column(Integer, default=0)
    findings_found = Column(Integer, default=0)
    assets_found = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)

    project = relationship("Project", back_populates="scans")
    raw_findings = relationship("RawFinding", back_populates="scan", cascade="all, delete-orphan")
    crypto_assets = relationship("CryptoAsset", back_populates="scan", cascade="all, delete-orphan")
    dependencies = relationship("Dependency", back_populates="scan", cascade="all, delete-orphan")
