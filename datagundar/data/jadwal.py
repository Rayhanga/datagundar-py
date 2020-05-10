from datagundar.utils.proxy import Proxy
from bs4 import BeautifulSoup as bs
import datetime

site = {

}

class Jadwal(Proxy):
    def __init__(self, site=site):
        super().__init__(site)

    # Get Jadwal Akademik
    # Get Jadwal Perkuliahan
    # Get Jadwal Pengisian KRS
    # Get Jadwal Ujian Utama
    # Get Jadwal Ujian Akhir Semester