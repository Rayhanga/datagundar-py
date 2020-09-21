from utils.proxy import OpenWeb

import re

website = {
    'TIMESTAMP': 'https://baak.gunadarma.ac.id/kuliahUjian/6',
    'JADKUL': lambda kelas: 'https://baak.gunadarma.ac.id/jadwal/cariJadKul?teks='+kelas.upper()
}

def getTimeStampLUT(proxy):
    result = []
    proxy.openPage(website['TIMESTAMP'])

    timeStampSauce = proxy.getSauce(expectedClassName='cell-xs-6')
    timeStampTable = timeStampSauce.find('table', {'class': 'cell-xs-6'})
    
    for row in timeStampTable.findAll('tr'):
        data = [datum.text.replace(' ', '').replace('.', ':').split('-') for datum in row.findAll('td')[1:]]
        if data:
            result.append(data[0])
        else:
            result.append(data)

    return result

def getJadwalKelas(kelas):
    with OpenWeb(website) as proxy:
        result = []
        timeStampLUT = getTimeStampLUT(proxy)

        proxy.openPage(website['JADKUL'](kelas.upper()))

        jadkulSauce = proxy.getSauce(expectedTagName='table')
        jadkulTitle = jadkulSauce.find('h5').text
        jadkulDescription = jadkulSauce.find('p', {'class': 'text-md-left'}).text
        jadkulTable = jadkulSauce.find('table')
        for row in jadkulTable.findAll('tr')[1:]:
            data = [datum.text for datum in row.findAll('td')[1:]]
            
            jadwalHari = data[0]
            jadwalMatkul = data[1]
            jadwalWaktu = data[2]
            jadwalRuang = data[3]
            jadwalDosen = data[4].title()

            if jadwalWaktu:
                jadwalWaktuStart = jadwalWaktu[0:1] if jadwalWaktu[1].isdigit() else jadwalWaktu[0]
                jadwalWaktuEnd = jadwalWaktu[-2:] if jadwalWaktu[-2].isdigit() else jadwalWaktu[-1]
                jadwalWaktu = timeStampLUT[int(jadwalWaktuStart)][0] + " - " + timeStampLUT[int(jadwalWaktuEnd)][1]

            result.append({
                'jadwalHari': jadwalHari,
                'jadwalMatkul': jadwalMatkul,
                'jadwalWaktu': jadwalWaktu,
                'jadwalRuang': jadwalRuang,
                'jadwalDosen': jadwalDosen
            })
        
        return result