from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from .database import Base, engine, get_db
from .seed import seed_data
from .routes import events, metrics
from fastapi.middleware.cors import CORSMiddleware
Base.metadata.create_all(bind=engine)

app=FastAPI(title="AI Productivity Dashboard")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(events.router)
app.include_router(metrics.router)

@app.post("/seed")
def seed(db: Session = Depends(get_db)):
    seed_data(db)
    return {"status":"seeded"}