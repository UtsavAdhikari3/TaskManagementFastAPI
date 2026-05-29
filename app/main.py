from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.session import get_db

app = FastAPI(
    title="Task Management RBAC API",
    version="1.0.0",
    description="Backend API system for task management with JWT authentication and role-based access control."
)


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/db-health")
def db_health_check(db: Session = Depends(get_db)):
    db.execute(text("SELECT 1"))
    return {"database": "connected"}