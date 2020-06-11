# restapi

`restapi` is based on `Flask` to serve data from `datagundar` module on a RESTful endpoint.

Available endpoints and metadata of expected result from said endpoint

_for more details on expected result metadata please refer to [`datagundar` README.md](https://github.com/Rayhanga/DataGundar/blob/master/datagundar/README.md)._

| Endpoint | Expected Result | Required Request Body |
| :-----: | :-----: | :-----: |
| `/api/jadwal/jadkul/<kelas>` | `Jadwal.getJadwalKelas(kelas)` | NONE |
| `/api/sap/<jurusan>` | `SAP.getDaftarJurusan()` | NONE |
| `/api/vclass/upcoming_tasks/` | `Vclass.getUpcomingTasks()` | `{'uname': [UsernameForVClass], 'pwd': [PasswordForVclass]}` |