from sqlalchemy import Column, String, Text
from database import Base

class AppConfig(Base):
    __tablename__ = "app_configurations"

    key = Column(String, primary_key=True, index=True)  # e.g., "homepage_alert_notice"
    value = Column(Text, nullable=True)
