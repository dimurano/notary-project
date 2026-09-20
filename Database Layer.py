import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Text
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class SessionStatus(str, enum.Enum):
    CREATED = "CREATED"
    WAITING_FOR_SIGNATURE = "WAITING_FOR_SIGNATURE"
    SIGNED = "SIGNED"
    COMPLETED = "COMPLETED" # Notary seal applied + saved to Cloud Storage
    EXPIRED = "EXPIRED"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    sessions = relationship("NotarySession", back_populates="client")

class NotarySession(Base):
    __tablename__ = "notary_sessions"

    id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Adobe Tracking References
    adobe_agreement_id = Column(String, unique=True, index=True, nullable=True)
    document_name = Column(String, nullable=False)
    gcs_raw_file_path = Column(String, nullable=False) # GCS bucket path for original PDF
    gcs_signed_file_path = Column(String, nullable=True) # GCS path for final sealed PDF
    
    status = Column(Enum(SessionStatus), default=SessionStatus.CREATED, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    client = relationship("User", back_populates="sessions")
