from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from vclass import getCourseData

class Credentials(BaseModel):
    username: str
    password: str

app = FastAPI()

@app.post("/api/vclass/")
async def getVclassData(credentials: Credentials, modifiedData: Optional[dict] = None):
    return getCourseData(credentials)

@app.get("/api/jadwal/{kelas}")
async def getJadwalKelas(kelas: str):
    kelas = kelas.upper()
    return(kelas)