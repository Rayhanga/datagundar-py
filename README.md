# Data Gundar

Data Gundar is a Python module to scrap and process data from Gunadarma's Website without any hassle.

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
### jadwalKelas
Get schedule for selected `kelas` using `jadwalKelas` module

```python
import datagundar

datagundar.jadwalKelas(kelas)
# returns a python dict of selected kelas
```

Expected Output:

```python
# datagundar.jadwalKelas([Kelas])
{
    "jadkul": [
        {
            "hari": ...,
            "matkul": ...,
            "jam": ...,
            "ruangan": ...,
            "dosen": ....
        },
        ....
    ],
    "meta": {
        "kelas": ...,
        "semester": ...,
        "tahun": ...,
        "berlaku_mulai": ....
    }
}
```

### sapJurusan

Get sap for selected `jurusan` using `sapJurusan` module

```python
import datagundar

jur = datagundar.sapJurusan(jurusan) 
# returns a python dict of selected jurusan
```

Expected Output:

```python
# datagundar.sapJurusan([NamaLengkapJurusan])
{
    "nama": ...,
    "url_value": ...,
    "jenjang": ...,
    "matkul": [
        {
            "judul": ...,
            "kode": ...,
            "wajib": [True / False],
            "semester": ...,
            "jenis": "UTAMA" / "LOKAL",
            "download_link":....
        },
        ....
    ]
}
```

_Example_:

```python
import datagundar as dg

# Get a python dict of both data and meta
jadwal = dg.jadwalKelas("2ia18")

# Output:
# {
#   "jadkul": ...,
#   "meta": ...
# }

# Get Teknik Informatika sap data and meta as a python dict
TI = dg.sapJurusan("Teknik Informatika")

# Output:
# {
#     "nama": ...,
#     "url_value": ...,
#     "jenjang": ...,
#     "matkul": [
#         {
#             "judul": ...,
#             "kode": ...,
#             "wajib": [True / False],
#             "semester": ...,
#             "jenis": "UTAMA" / "LOKAL",
#             "download_link":....
#         },
#         ....
#     ]
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[GNU GPLv3.0](https://github.com/Rayhanga/DataGundar/blob/master/LICENSE)
