from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from sentinel.schemas.incident import IncidentRead, IncidentCreate, IncidentUpdate
from sentinel.db.session import get_db
from sentinel.models.incident import Incident

router = APIRouter(prefix="/incidents", tags=["incidents"])

@router.post("", response_model=IncidentRead, status_code=201)
def create_incident(
    payload: IncidentCreate,
    db: Annotated[Session, Depends(get_db)],
):
    incident = Incident(**payload.model_dump())
    db.add(incident)
    db.commit()
    db.refresh(incident)
    return incident 

@router.get("", response_model=list[IncidentRead])
def get_incidents(db: Annotated[Session, Depends(get_db)]):
    return db.scalars(select(Incident)).all()


@router.get("/{incident_id}", response_model=IncidentRead)
def get_incident(incident_id: int, db: Annotated[Session, Depends(get_db)]):
    incident = db.get(Incident, incident_id)

    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")

    return incident 

@router.patch("/{incident_id}", response_model=IncidentRead)
def update_incident(
    incident_id:int, 
    payload: IncidentUpdate, 
    db:Annotated[Session, Depends(get_db)]):
    
    incident = db.get(Incident, incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    updates = payload.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(incident, field, value) 
    
    db.commit()
    db.refresh(incident)
    return incident 

@router.delete("/{incident_id}", status_code=204)
def delete_incident(incident_id:int, db:Annotated[Session, Depends(get_db)]):
    incident = db.get(Incident, incident_id)
    if incident is None:
        raise HTTPException(status_code=404, detail="Incident not found")
    
    db.delete(incident)
    db.commit()