from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from sql_app.database import SessionLocal, engine

from sql_app import crud, models, schemas

models.Base.metadata.create_all(bind=engine)

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

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email is already in use")
    return crud.create_user(db=db, user=user)
    
@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.get_users(db, skip=skip, limit=limit)
    return users

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    print(type(db_user))
    return db_user

@app.post("/users/{user_id}/projects/", response_model=schemas.Project)
def create_project_for_user(
    user_id: int, project: schemas.ProjectCreate, db: Session = Depends(get_db)
):
    return crud.create_user_project(db=db, project=project, user_id=user_id)

@app.get("/projects/", response_model=list[schemas.Project])
def read_projects(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    projects = crud.get_projects(db, skip=skip, limit=limit)
    return projects
