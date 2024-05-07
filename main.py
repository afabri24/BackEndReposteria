

from fastapi import FastAPI
from router.router import api_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "http://localhost:5173", "http://localhost:5174", #Permitir solicitudes desde este origen
    # Se puede agragar más origines si es necesario

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)