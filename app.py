from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from data.vclass import getCourseData
from data.fakultas import getFakultasList, getMajorSAP
from data.jadwal import getJadwalKelas
from data.staff import getStaffList, getStaffInfo

class Credentials(BaseModel):
    username: str
    password: str

app = FastAPI()

@app.post("/api/vclass/")
async def vclass_data(credentials: Credentials):
    return getCourseData(credentials)

@app.get("/api/fakultas/")
async def fakultas_list():
    return getFakultasList()

@app.get("/api/sap/{fakultas}/")
async def sap_fakultas(fakultas: str):
    return getMajorSAP(fakultas)

@app.get("/api/jadwal/{kelas}/")
async def jadwal_kelas(kelas: str):
    return(getJadwalKelas(kelas))

@app.get("/api/staff/")
async def staff_list():
    return(getStaffList())

@app.get("/api/staff/{staff_name}")
async def staff_info(staff_name: str):
    return(getStaffInfo(staff_name))