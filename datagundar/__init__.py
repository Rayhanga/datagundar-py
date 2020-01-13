from .data import jadwal, sap

def jadwalKelas(kelas):
    return {
        "data": jadwal.cipetjadwal(kelas),
        "meta": jadwal.cipetmeta(kelas) 
    }

def sapJurusan(jurusan):
    return sap.getmajorfromlist(jurusan)