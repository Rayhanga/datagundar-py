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
        major['matkul'].append({
            'judul' : x.findChildren("td")[1].getText(),
            'kode' : x.findChildren("td")[0].getText(),
            'detail_url' : x.findChildren("td")[2].findChildren("a")[0]['href'].replace("?stateid=", ""),
            'download_link' : x.findChildren("td")[2].findChildren("a")[1]['href']
        })