from fastapi import FastAPI
from router.router import usuario_router

app = FastAPI()


app.include_router(usuario_router)