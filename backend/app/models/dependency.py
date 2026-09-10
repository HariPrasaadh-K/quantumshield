from sqlalchemy import Column, String, Text, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.core.database import Base

class Dependency(Base):
    __tablename__ = "dependencies"

    id = Column(String, primary_key=True, index=True)
    scan_id = Column(String, ForeignKey("scans.id", ondelete="CASCADE"), nullable=False)
    source_asset_id = Column(String, nullable=False)
    target_asset_id = Column(String, nullable=False)
    relationship_type = Column(String, nullable=False) # USES, IMPLEMENTS, IMPORTS, DEPENDS_ON, PROTECTS, CONFIGURES
    confidence = Column(Float, default=0.8)
    evidence = Column(Text, nullable=True)

    scan = relationship("Scan", back_populates="dependencies")
