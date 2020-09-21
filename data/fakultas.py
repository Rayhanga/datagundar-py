from utils.proxy import OpenWeb

import re

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
    with OpenWeb(website) as proxy:
        result = []

        proxy.clickLink('Daftar SAP')
        proxy.getSauce(expectedClassName='col-md-6')
        proxy.clickLink(majorName)
        sapSauce = proxy.getSauce(expectedId='dafsap')
        for i, tr in enumerate(sapSauce.findAll('tr')[1:]):
            proxy.waitForElement('Details')
            detailLinks = proxy.driver.find_elements_by_partial_link_text('Details')
            detailLinks[i].click()
            detailSauce = proxy.getSauce(expectedClassName='col-md-12')

            sapData = detailSauce.findAll('td')
            sapId = sapData[1].text
            sapTitle = sapData[3].text
            sapLocality = sapData[5].text
            sapType = sapData[7].text
            sapDescription = sapData[9].text
            
            proxy.driver.back()
            
            result.append({
                'sapID': sapId,
                'sapTitle': sapTitle,
                'sapLocality': sapLocality,
                'sapType': sapType,
                'sapDescription': sapDescription
            })     

        return result