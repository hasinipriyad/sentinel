from datetime import datetime
from pydantic import BaseModel, Field, ConfigDict
from sentinel.models.incident import Severity, Status

class IncidentCreate(BaseModel):
    title: str = Field(max_length=200)
    description: str
    severity: Severity
    service: str = Field(max_length=100)

class IncidentRead(IncidentCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int
    status: Status
    created_at: datetime
    updated_at: datetime

class IncidentUpdate(BaseModel):
    title: str | None = Field(default=None, max_length=200)
    description: str | None = None 
    severity: Severity | None = None 
    status: Status | None = None 
    service: str | None = Field(default=None, max_length=100) 