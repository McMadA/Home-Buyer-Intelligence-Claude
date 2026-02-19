import uuid
from datetime import datetime
from sqlalchemy import Column, String, Float, Integer, Boolean, Text, DateTime, JSON, Enum as SAEnum
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

class SessionModel(Base):
    __tablename__ = "sessions"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = Column(DateTime, default=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)

class DocumentModel(Base):
    __tablename__ = "documents"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), nullable=False, index=True)
    filename = Column(String(255), nullable=False)
    document_type = Column(String(50), default="other")
    file_path = Column(String(500), nullable=False)
    file_size_bytes = Column(Integer, default=0)
    extracted_text = Column(Text, nullable=True)
    parsed_data = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class PropertyModel(Base):
    __tablename__ = "properties"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), nullable=False, index=True)
    address = Column(String(255), nullable=True)
    postal_code = Column(String(10), nullable=True)
    city = Column(String(100), nullable=True)
    square_meters = Column(Float, nullable=True)
    year_built = Column(Integer, nullable=True)
    energy_label = Column(String(5), nullable=True)
    property_type = Column(String(50), nullable=True)
    asking_price = Column(Float, nullable=True)
    hoa_monthly_cost = Column(Float, nullable=True)
    num_rooms = Column(Integer, nullable=True)
    has_garden = Column(Boolean, nullable=True)
    has_parking = Column(Boolean, nullable=True)
    bag_id = Column(String(50), nullable=True)

class AnalysisResultModel(Base):
    __tablename__ = "analysis_results"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), nullable=False, index=True)
    status = Column(String(20), default="pending")
    property_data = Column(JSON, nullable=True)
    strengths = Column(JSON, nullable=True)
    weaknesses = Column(JSON, nullable=True)
    risk_score = Column(JSON, nullable=True)
    market_position = Column(JSON, nullable=True)
    bidding_advice = Column(JSON, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)
    error_message = Column(Text, nullable=True)

class AuditLogModel(Base):
    __tablename__ = "audit_logs"
    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    session_id = Column(String(36), nullable=True, index=True)
    action = Column(String(100), nullable=False)
    resource_type = Column(String(50), nullable=True)
    resource_id = Column(String(36), nullable=True)
    details = Column(JSON, nullable=True)
    ip_address = Column(String(45), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
