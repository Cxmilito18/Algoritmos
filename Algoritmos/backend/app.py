from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from controller import ordenar_algoritmo

app = FastAPI()

# CORS para que React pueda hablar con FastAPI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Datos(BaseModel):
    valores: list[int]
    algoritmo: str

@app.post("/ordenar")
def ordenar(datos: Datos):
    pasos = ordenar_algoritmo(datos.valores, datos.algoritmo)
    return {"pasos": pasos}
