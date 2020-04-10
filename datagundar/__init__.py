from .data import jadwal, sap
from .utils import archiver
import os, json

dir_path = os.path.dirname(os.path.realpath(__file__))
arc_path = dir_path+'/archives/'
jad_path = arc_path+'jadwal/'
sap_path = arc_path+'sap/'
if not os.path.exists(arc_path):
    os.makedirs(arc_path)

def jadwalKelas(kelas, force_update=False):
    if not os.path.exists(jad_path):
        os.makedirs(jad_path)
    data_tag='JADWAL_'+kelas.upper()
    
    try:
        if force_update:
            raise Exception
        # print("Searching Archive")
        json_data = archiver.getArchiveData(data_tag, jad_path)
        staged_data = json.loads(json_data['data'])
        matkul = staged_data['matkul']
        meta = staged_data['meta']
    except:
        # print("Getting Data from web")
        matkul = jadwal.cipetjadwal(kelas)
        meta = jadwal.cipetmeta(kelas)
        staged_data = {
            "matkul": matkul,
            "meta": meta
        }
        archiver.postArchiveData(staged_data, data_tag, jad_path)

    return {
        "matkul": matkul,
        "meta": meta
    }

def sapJurusan(jurusan, force_update=False):
    if not os.path.exists(sap_path):
        os.makedirs(sap_path)
    data_tag='SAP_'+jurusan.upper().replace(" ", "")
    
    try:
        if force_update:
            raise Exception
        # print("Searching Archive")
        staged_data = archiver.getArchiveData(data_tag, sap_path)['data']
    except:
        # print("Getting Data from web")
        staged_data = sap.getmajorfromlist(jurusan)
        archiver.postArchiveData(staged_data, data_tag, sap_path)
    
    return staged_data