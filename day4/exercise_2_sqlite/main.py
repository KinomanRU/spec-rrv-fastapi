from contextlib import asynccontextmanager

from fastapi import FastAPI
from models import create_tables
from routers import books_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(books_router)


# Index
@app.get("/")
async def index():
    return {"message": "Welcome to BookDB"}
