from enum import Enum
from datetime import datetime

from sqlalchemy import Enum as SAEnum, String, Text, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column 

from sentinel.db.base import Base

class Severity(str,Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"

class Status(str,Enum):
    OPEN = "open"
    INVESTIGATING = "investigating"
    RESOLVED = "resolved"

class Incident(Base):
    __tablename__ = "incidents"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    severity: Mapped[Severity] = mapped_column(SAEnum(Severity, values_callable=lambda e:[m.value for m in e]))
    status: Mapped[Status] = mapped_column(SAEnum(Status, values_callable=lambda e:[m.value for m in e]))
    service: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())