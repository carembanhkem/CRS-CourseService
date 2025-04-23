from contextlib import asynccontextmanager
from typing import Union

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api.courses import course_router as courses_router
from api.lectures import lecture_router as lecture_router
from api.auth import auth_router as auth_router
from api.db.session import (
    init_db,
    insert_heroes_from_json,
    is_heroes_table_empty_or_missing,
)
import sys

print("Running Python from:", sys.executable)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # before app start up
    init_db()

    if is_heroes_table_empty_or_missing():
        insert_heroes_from_json("api/db/heroes.json")
    yield
    # clean up


app = FastAPI(
    title="Gaming Course Recommendation System",
    description="LMS for managing students and courses.",
    version="0.0.1",
    contact={
        "name": "carembanhkem",
        "email": "nhattan.ezvisa@gmail.com",
    },
    license_info={
        "name": "MIT",
    },
    lifespan=lifespan,
)

origins = ["http://localhost", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(courses_router, prefix="/api/courses", tags=["courses"])
app.include_router(lecture_router, prefix="/api/lectures", tags=["lectures"])
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])


@app.get("/")
def read_root():
    return {"Hello": "Worlder"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/healthz")
def read_api_health():
    return {"status": "ok"}
