from sqlalchemy import Column, String, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class Recommendation(Base):
    __tablename__ = "recommendations"

    id = Column(String, primary_key=True, index=True)
    asset_id = Column(String, ForeignKey("crypto_assets.id", ondelete="CASCADE"), nullable=False, unique=True)
    current_algorithm = Column(String, nullable=False)
    current_purpose = Column(String, nullable=False)
    candidate_algorithm = Column(String, nullable=False)
    reason = Column(Text, nullable=False)
    migration_complexity = Column(String, default="Medium")
    performance_considerations = Column(Text, nullable=True)
    compatibility_considerations = Column(Text, nullable=True)
    confidence = Column(Float, default=0.9)
    disclaimer = Column(Text, nullable=False)

    asset = relationship("CryptoAsset", back_populates="recommendation")
