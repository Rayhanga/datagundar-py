from datagundar.utils.proxy import Proxy
from bs4 import BeautifulSoup as bs
import datetime

site = {
    'MAIN': 'https://baak.gunadarma.ac.id/',
    'TIMESTAMP': 'https://baak.gunadarma.ac.id/kuliahUjian/6',
    'JADKUL': lambda kelas: 'https://baak.gunadarma.ac.id/jadwal/cariJadKul?teks='+kelas.upper()
}

class Jadwal(Proxy):
    def __init__(self, site=site):
        super().__init__(site)
        self.timeStamp = self.getTimeStamp()

    # Get Timestamp Data
    def getTimeStamp(self):
        self.openPage(site['TIMESTAMP'])
        sauce = bs(self.driver.page_source, 'html.parser')
        rows = sauce.find('table', {'class': 'table table-custom table-primary table-fixed stacktable cell-xs-6'}).findChildren('tr')
        timeStamp = []

        for row in rows:
            data = row.findAll('td')
            if data:
                stamp = data[0].text.strip()[-2:].strip()
                start = data[1].text.strip()[:5].replace('.', ':')
                end = data[1].text.strip()[-5:].replace('.', ':')
                
                timeStamp.append({
                    'start': start,
                    'end': end
                })

        return timeStamp
                           
    # Get Jadwal Perkuliahan
    def getJadwalKelas(self, kelas):
        self.openPage(site['JADKUL'](kelas))
        sauce = bs(self.driver.page_source, 'html.parser')
        rows = sauce.findAll('tr')[1:]
        res = {}

        if 'tidak ada' in sauce.find('h5').text:
            return None
            
        for row in rows:
            data = row.findAll('td')[1:]
            
            if data:
                hari = data[0].text
                matkul = data[1].text
                waktu = data[2].text
                ruang = data[3].text
                dosen = data[4].text

                waktu = self.timeStamp[int(waktu[:2].strip('/'))-1]['start'] + ' - ' + self.timeStamp[int(waktu[-2:].strip('/'))-1]['end']

                try:
                    if res[hari]:
                        pass
                except:
                    res[hari] = []

                res[hari].append({
                    'waktu': waktu,
                    'matkul': matkul,
                    'ruang': ruang,
                    'dosen': dosen
                })

        return res

    # Get Jadwal Akademik
    # def getJadwalAkademik(self):
    #     self.openPage(self.site['MAIN'])
    #     sauce = bs(self.driver.page_source, 'html.parser')

    #     table = sauce.find('table', {'class': 'table table-custom table-primary bordered-table table-striped table-fixed stacktable large-only'}).find('tbody')
    #     rows = table.findChildren('tr')

    #     for row in rows:
    #         data = row.findChildren('td')
    #         header = False
    #         if len(data) > 0:
    #             kgtn = data[0].text.strip()
    #             tgl = data[1].text.strip()
    #             thn = tgl[-4:]
    #             print(kgtn, tgl)

    # Get Jadwal Pengisian KRS
    # Get Jadwal Ujian Utama
    # Get Jadwal Ujian Akhir Semester