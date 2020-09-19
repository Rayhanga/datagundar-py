from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from vclass import getCourseData
from fakultas import getFakultasList, getMajorSAP

class Credentials(BaseModel):
    username: str
    password: str

app = FastAPI()

@app.post("/api/vclass/")
async def vclassData(credentials: Credentials):
    return getCourseData(credentials)

@app.get("/api/fakultas/")
async def fakultasList():
    return getFakultasList()

@app.get("api/sap/{fakultas}/")
async def fakultasSap(fakultas: str):
    return getMajorSAP(fakultas)

@app.get("/api/jadwal/{kelas}/")
async def jadwalKelas(kelas: str):
    kelas = kelas.upper()
    return(kelas)