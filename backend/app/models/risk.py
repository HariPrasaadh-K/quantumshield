import datetime
from sqlalchemy import Column, String, DateTime, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(String, primary_key=True, index=True)
    asset_id = Column(String, ForeignKey("crypto_assets.id", ondelete="CASCADE"), nullable=False, unique=True)
    quantum_vulnerability_score = Column(Float, default=0.0)
    data_sensitivity_score = Column(Float, default=0.0)
    data_lifetime_score = Column(Float, default=0.0)
    business_criticality_score = Column(Float, default=0.0)
    migration_difficulty_score = Column(Float, default=0.0)
    total_score = Column(Float, default=0.0)
    risk_type = Column(String, default="Unknown")
    explanation = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    asset = relationship("CryptoAsset", back_populates="risk_assessment")
