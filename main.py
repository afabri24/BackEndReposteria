from fastapi import FastAPI
from router.router import api_router

app = FastAPI()


app.include_router(api_router)