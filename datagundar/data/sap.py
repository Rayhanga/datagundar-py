from datagundar.utils.proxy import Proxy
from bs4 import BeautifulSoup as bs
import time

site = {
    'MAIN': 'https://sap.gunadarma.ac.id/'
}

class SAP(Proxy):
    def __init__(self, site=site):
        super().__init__(site)

    def getDaftarJurusan(self):
        self.openPage(self.site['MAIN'])
        self.driver.find_element_by_link_text('Daftar SAP').click()
        res = {}

        time.sleep(1)
        sauce = bs(self.driver.page_source, 'html.parser')

        fakultas = None
        for item in sauce.findAll('li'):
            if item.attrs.get('class'):
                fakultas = item.text.strip()
                res[fakultas] = []
            else:  
                jurusan = item.text.strip()
                namaJurusan = jurusan.strip('D3').strip('S1')
                jenjangJurusan = jurusan[-2:]
                res[fakultas].append({
                    'jurName': namaJurusan,
                    'jurDegree': jenjangJurusan
                })

        return res

    def getSAPJurusan(self, jurusan):
        jurusan = jurusan.strip()
        self.openPage(self.site['MAIN'])
        self.driver.find_element_by_link_text('Daftar SAP').click()
        time.sleep(1)
        self.driver.find_element_by_partial_link_text(jurusan).click()
        time.sleep(1)

        res = []

        sauce = bs(self.driver.page_source, 'html.parser')
        for i, item in enumerate(sauce.findAll('tr')[1:]):
            detailLinks = self.driver.find_elements_by_partial_link_text('Details')

            detailLinks[i].click()
            time.sleep(1)
            detailSauce = bs(self.driver.page_source, 'html.parser')

            details = detailSauce.find('div', {'class': 'col-md-12'}).findChildren('tr')[:-1]
            for i, det in enumerate(details):
                data = det.findChildren('td')[1].text
                if i == 0:
                    sapCode = data
                elif i == 1:
                    sapName = data
                elif i == 2:
                    if 'Negara' in data:
                        sapLocality = 'Utama'
                    if 'Lokal' in data:
                        sapLocality = 'Lokal'
                elif i == 3:
                    sapType = data
                elif i == 4:
                    sapSemester = None
                    if 'softskill' in data:
                        sapType = sapType + ' (Softskill)'
                    if 'semester' in data:
                        sapSemester = data.lower().strip(', sebagai matakuliah softskill').strip('ditawarkan di semester').strip(', wajib diambil oleh semua mahasiswa').strip()

            res.append({
                'sapCode': sapCode,
                'sapName': sapName,
                'sapSemester': sapSemester,
                'sapLocality': sapLocality,
                'sapType': sapType
            })
            
            self.driver.back()
            time.sleep(1)

        try: 
            res = sorted(res, key=lambda k: k['sapSemester'])
        except:
            temp = []
            for i, item in enumerate(res):
                if not item['sapSemester']:
                    temp.append(item)
            res = sorted([a for a in res if a not in temp], key=lambda k: k['sapSemester']) + temp

        return res