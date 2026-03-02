from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from ..database import get_db
from ..models import Event
from ..schemas import EventCreate

router = APIRouter()

@router.post("/events")
def ingest(event: EventCreate, db: Session = Depends(get_db)):
    obj = Event(**event.dict())
    db.add(obj)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(400, "Duplicate event ignored")
    return {"status":"stored"}