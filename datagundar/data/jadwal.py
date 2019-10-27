from ..utils import scrapper

# Variable declarations
url = "https://baak.gunadarma.ac.id/jadwal/cariJadKul"
url_para = "teks"
jam_dataset = []

# Dataset for default timeset
for i in range(1, 14):
    if i > 3:
        a = '%s:30' % (i+6)
    else:
        a = '0%s:30' % (i+6)
    if i > 2:
        b = '%s:30' % (i+7)
    else:
        b = '0%s:30' % (i+7)
    jam_dataset.append({
        'awal' : a,
        'akhir' : b
    })

# Get schedule in Python Dict format
def cipetjadwal(kelas):
    soup = scrapper.httpgetsoup(url, url_para, kelas)
    table = soup.find('table', attrs={'class':'table'}).findAll('td')

    jadwal = []
    hari = scrapper.scraptable(table, 6, 1)
    matkul = scrapper.scraptable(table, 6, 2)
    jam = scrapper.scraptable(table, 6, 3)
    ruangan = scrapper.scraptable(table, 6, 4)
    dosen = scrapper.scraptable(table, 6, 5)

    for i in range(len(hari)):
        x = jam_dataset[int(jam[i][0])-1]['awal']
        y = jam_dataset[int(jam[i][-1:])-1]['akhir']
        jadwal.append({
            'hari' : hari[i],
            'matkul' : matkul[i],
            'jam' : '%s - %s' % (x, y),
            'ruangan' : ruangan[i],
            'dosen' : dosen[i]
        })

    return jadwal

# Get meta for current schedule in Python Dict format
def cipetmeta(kelas):
    soup = scrapper.httpgetsoup(url, url_para, kelas)
    x = soup.find('h5').text
    y = soup.find('p', attrs={'class':'text-md-left'}).text
    if "PTA" in x:
        semester = "PTA"
    elif "ATA" in x:
        semester = "ATA"
    else:
        semester = ""
    kelas = soup.find('b').text.upper()
    tahun = x[-10:].replace("/","-").strip()
    berlaku_mulai = y.replace('Berlaku Mulai : ', "")
    data = {
        'kelas' : kelas,
        'semester' : semester,
        'tahun' : tahun,
        'berlaku_mulai' : berlaku_mulai
    }
    return data