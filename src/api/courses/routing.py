from fastapi import APIRouter, Depends

router = APIRouter()

@router.get("/")
def read_courses():
    return {"courses": "List of courses"}