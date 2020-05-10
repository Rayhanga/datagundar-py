from datagundar.utils.proxy import Proxy
from bs4 import BeautifulSoup as bs

site = {
    # https://sap.gunadarma.ac.id/
}

class SAP(Proxy):
    def __init__(self, site=site):
        super().__init__(site)

    # Get Daftar Jurusan
    # Get SAP Jurusan