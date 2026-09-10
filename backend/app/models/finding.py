from sqlalchemy import Column, String, Text, Integer, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from app.core.database import Base

class RawFinding(Base):
    __tablename__ = "raw_findings"

    id = Column(String, primary_key=True, index=True)
    scan_id = Column(String, ForeignKey("scans.id", ondelete="CASCADE"), nullable=False)
    detector = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    line_number = Column(Integer, nullable=False)
    matched_text = Column(Text, nullable=False)
    surrounding_context = Column(Text, nullable=True)
    language = Column(String, nullable=True)
    algorithm_hint = Column(String, nullable=True)
    library_hint = Column(String, nullable=True)
    confidence = Column(Float, default=0.5)
    finding_metadata = Column(JSON, nullable=True)

    scan = relationship("Scan", back_populates="raw_findings")
