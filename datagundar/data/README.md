# datagundar
`datagundar` has multiple modules, each modules will create a new _headless proxy_ of it's own. And each modules are a Class inherited from the `Proxy` Class.

API for `datagundar` module 

```python
from datagundar import Jadwal
from datagundar import SAP
from datagundar import Vclass

Jadwal.getJadwalKelas(kelas)
# returns a dictionary of jadwal for selected kelas

# metadata:
{
  Hari: [
    {
      'waktu': String,
      'matkul': String,
      'ruang': String,
      'dosen': String
    },
    ...
  ],
  ...
}


SAP.getDaftarJurusan()
# returns a dictionary of available Jurusan

# metadata:
{
  Fakultas: [
    {
      'jurName': String,
      'jurDegree': String,
    },
    ...,
  ],
  ...
}

SAP.getSAPJurusan(jurusan)
# returns a list of SAPs for selected jurusan 
# (sorted from the smallest sapSemester)

# metadata:
[
  {
    'sapCode': String,
    'sapName': String,
    'sapSemester': String,
    'sapLocality': String,
    'sapType': String
  },
  ...
]


Vclass.getUpcomingTasks()
# returns a list of upcoming tasks
# (sorted from the nearest deadline)

# metadata:
[
  {
    'actTitle': String,
    'actLink': String,
    'actType': String,
    'actComplete': String,
    'actStart': datetime,
    'actDeadline': datetime
  },
  ...
]
```