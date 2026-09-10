import datetime
from sqlalchemy import Column, String, DateTime, Text, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class CryptoAsset(Base):
    __tablename__ = "crypto_assets"

    id = Column(String, primary_key=True, index=True)
    scan_id = Column(String, ForeignKey("scans.id", ondelete="CASCADE"), nullable=False)
    name = Column(String, nullable=False)
    algorithm = Column(String, nullable=False)
    crypto_purpose = Column(String, default="Unknown")
    purpose_confidence = Column(Float, default=0.5)
    file_path = Column(String, nullable=False)
    line_number = Column(Integer, default=1)
    language = Column(String, nullable=True)
    library = Column(String, nullable=True)
    risk_type = Column(String, default="Unknown") # Quantum, Classical, Monitor, Unknown
    risk_score = Column(Float, default=0.0)
    priority = Column(String, default="P3") # P0, P1, P2, P3
    
    # Editable Context Inputs
    data_sensitivity = Column(String, default="Medium") # Low, Medium, High, Critical
    business_criticality = Column(String, default="Medium") # Low, Medium, High, Critical
    data_lifetime_years = Column(Integer, default=10)
    migration_difficulty = Column(String, default="Medium") # Low, Medium, High
    
    status = Column(String, default="active")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    scan = relationship("Scan", back_populates="crypto_assets")
    risk_assessment = relationship("RiskAssessment", back_populates="asset", uselist=False, cascade="all, delete-orphan")
    recommendation = relationship("Recommendation", back_populates="asset", uselist=False, cascade="all, delete-orphan")
