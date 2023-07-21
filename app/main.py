from fastapi import FastAPI
from app.database.base import engine, SessionLocal, Base
from app.models import Menu, SubMenu, Dish

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
