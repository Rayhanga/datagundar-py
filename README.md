# Data Gundar

Data Gundar is a collection of Python modules to scrap and process data from Gunadarma's Website without any hassle.

***Disclaimer***: This modules ignore robots.txt, _use it at your own risk_.

## Installation

Install `virtualenv`:

```bash
pip install virtualenv
```

Create new `virtualenv` and install depedencies:

```bash
virtualenv venv &&
. venv/bin/activate && 
pip install -r requirements.txt
```

## Usage

Always use `virtualenv` when interacting with these modules

```bash
. venv/bin/activate
```

Get schedule for selected `kelas` using `jadwal` module

```python
from datagundar.data import jadwal

jadwal.cipetjadwal(kelas) # returns an array of schedule for selected kelas
jadwal.cipetmeta(kelas) # returns an array of meta for selected kelas schedules
```

Expected Output:

```python
# datagundar.data.jadwal.cipetjadwal()
[
    {
        "hari": ...,
        "matkul": ...,
        "jam": ...,
        "ruangan": ...,
        "dosen": ....
    },
    ....
]

# datagundar.data.jadwal.cipetmeta()
{
    "kelas": ...,
    "semester": ...,
    "tahun": ...,
    "berlaku_mulai": ....
}
```

Get sap for selected `jurusan` using `sap` module

```python
from datagundar.data import sap

jur = sap.getmajorfromlist(jurusan) # returns a python dict of selected jurusan
```

Expected Output:

```python
# datagundar.data.sap.getmajorfromlist()
{
    "nama": ...,
    "url_value": ...,
    "jenjang": ...,
    "matkul": [
        {
            "judul": ...,
            "kode": ...,
            "detail_url": ...,
            "download_link":....
        },
        ....
    ]
}
```

*Example:*

```python
from datagundar.data import jurusan, sap

# Get an array of schedule for 2ia18
jadwal_2ia18 = jadwal.cipetjadwal("2ia18")

# Get an array of meta for 2ia18 schedule
jadwal.cipetmeta("2ia18")

# Get Teknik Informatika meta and sap list as Python Dictionary
# And assign it to variable called TI
TI = sap.getmajorfromlist("Teknik Informatika")
```

_Simplified_:

```python
import datagundar as dg

# Get a python dict of both data and meta
jadwal = dg.jadwalKelas("2ia18")

# Output:
# {
#   "data": jadwal,
#   "meta": meta
# }

# Get Teknik Informatika sap data and meta as a python dict
TI = dg.sapJurusan("Teknik Informatika")
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[GNU GPLv3.0](https://github.com/Rayhanga/DataGundar/blob/master/LICENSE)
