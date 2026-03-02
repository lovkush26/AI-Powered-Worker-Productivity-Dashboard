from datetime import datetime, timedelta
import random
from sqlalchemy.orm import Session
from .models import Worker, Workstation, Event

def seed_data(db: Session):
    db.query(Event).delete()
    db.query(Worker).delete()
    db.query(Workstation).delete()

    workers=[Worker(worker_id=f"W{i}",name=f"Worker {i}") for i in range(1,7)]
    stations=[Workstation(station_id=f"S{i}",name=f"Station {i}") for i in range(1,7)]
    db.add_all(workers+stations)
    db.commit()

    base=datetime.utcnow()
    events=[]

    for i in range(600):
        events.append(Event(
            timestamp=base+timedelta(seconds=i*40),
            worker_id=f"W{random.randint(1,6)}",
            workstation_id=f"S{random.randint(1,6)}",
            event_type=random.choice(["working","idle","product_count"]),
            confidence=round(random.uniform(0.85,0.99),2),
            count=random.randint(1,6)
        ))

    db.add_all(events)
    db.commit()