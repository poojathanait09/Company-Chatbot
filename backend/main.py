from fastapi import FastAPI
from database import Base, engine
from routes import login, chat

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(login.router)
app.include_router(chat.router)