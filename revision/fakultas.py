from proxy import OpenWeb

from definitions import SAP_DIR

import re
import os

website = {
    'MAIN': 'https://sap.gunadarma.ac.id/'
}

def getFakultasList():
    with OpenWeb(website) as proxy:
        result = []

        proxy.clickLink('Daftar SAP')
        fakultasSauce = proxy.getSauce(expectedClassName='col-md-6')
        fakultasList = fakultasSauce.findAll('div', {'class': 'col-md-6'})

        for fakultas in fakultasList:
            fakultasName = fakultas.find('li', {'class': 'Fakultas'}).text
            jurusanList = [re.sub(r"(^\W|\W$)", "", jurusan.text) for jurusan in fakultas.findChildren('li')[1:]]

            result.append({
                'fakultasName': fakultasName,
                'fakultasMajors': jurusanList
            })

        return result

def getMajorSAP(majorName):
    downloadDir = os.path.join(SAP_DIR, majorName.title().replace(' ', ''))
    with OpenWeb(website, downloadDir=downloadDir) as proxy:
        result = []

        proxy.clickLink('Daftar SAP')
        proxy.getSauce(expectedClassName='col-md-6')
        proxy.clickLink(majorName)
        sapSauce = proxy.getSauce(expectedId='dafsap')
        for i, tr in enumerate(sapSauce.findAll('tr')[1:]):
            sapData = [td for td in tr.findAll('td')]

            sapId = sapData[0].text
            sapTitle = re.sub(r"(\/|\*+|#|\((\w|\d|\s)+\)|(RPS 2018))", "", sapData[1].text)
            print(sapTitle)
            
    
# for fakultas in getFakultasList():
#     print(fakultas)

getMajorSAP('Akuntansi S1')