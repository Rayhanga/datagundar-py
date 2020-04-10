from ..utils import scrapper

# Variable declarations
url="https://sap.gunadarma.ac.id/indexlama.php"
url_para = "stateid"

major_index = []

def updatemajorindex():
    soup = scrapper.httpgetsoup(url, url_para, 'daftar')
    majors = soup.findAll('a', {'class':'c3'})
    for major in majors:
        if major['href'].startswith("?"):
            major_index.append({
                'nama' : major.getText()[:-5],
                'url_value' :  major['href'].replace('?stateid=',''),
                'jenjang' : major.getText()[-2:],
                'matkul' : []
            })

def getmajorfromlist(major_name):
    if major_index:
        b = major_name.replace(" ","").lower()
        for m in major_index:
            a = m['nama'].replace(" ","").lower()
            if a == b:
                cipetsaplist(m)
                return m
    else:
        updatemajorindex()
        return getmajorfromlist(major_name) 

def cipetsaplist(major):
    soup = scrapper.httpgetsoup(url, url_para, major['url_value'])
    table = soup.find("table", { "width" : "98%" }).findChild("tbody").findChildren("tr")
    
    iterlist_table = iter(table)
    next(iterlist_table)
    for x in iterlist_table:
        judul = x.findChildren("td")[1].getText()
        kode = x.findChildren("td")[0].getText()
        download_link = x.findChildren("td")[2].findChildren("a")[1]['href']
        detail_param = x.findChildren("td")[2].findChildren("a")[0]['href'].replace("?stateid=", "")

        detailSoup = scrapper.httpgetsoup(url, url_para, detail_param)
        details=detailSoup.find("table", {"width": "90%"}).find("tbody").findChildren("td")
        details=details[5:-8]
    
        jenis = "UTAMA"
        if "Lokal" in details[1].text:
            jenis = "LOKAL"
        wajib = "Wajib" in details[3].text
        semester = details[5].text[-1:]

        major['matkul'].append({
            'judul' : judul,
            'kode' : kode,
            'wajib' : wajib,
            'semester': semester,
            'jenis': jenis,
            'download_link' : download_link
        })