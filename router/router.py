from fastapi import APIRouter

user_router = APIRouter()

@user_router.get("/")
def root():
    return {"message": "Hi, I'm the user router!"}