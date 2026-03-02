from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import Event
from ..metrics import compute_metrics

router = APIRouter()

@router.get("/metrics")
def get_metrics(db: Session = Depends(get_db)):
    events=db.query(Event).all()
    return compute_metrics(events)