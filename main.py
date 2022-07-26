from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def root(db: Session = Depends(get_db)):
    return {"The server is live!"}
