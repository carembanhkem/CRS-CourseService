from typing import Union

from fastapi import FastAPI
from api.courses import router as courses_router

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
)
app.include_router(courses_router, prefix="/api/courses", tags=["courses"])


@app.get("/")
def read_root():
    return {"Hello": "Worlder"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.get("/healthz")
def read_api_health():
    return {"status": "ok"}
