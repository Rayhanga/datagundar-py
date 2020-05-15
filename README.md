# Data Gundar

Data Gundar is a Python module to scrap and process data from Gunadarma's Website without any hassle.

## Installation

Install `virtualenv`:

```bash
pip install virtualenv
```

Create new `virtualenv` and install depedencies:

- Windows:

    ```
    virtualenv venv
    venv\Scripts\activate
    pip install -r requirements.txt
    ```

- Linux / MacOS:

    ```bash
    virtualenv venv &&
    . venv/bin/activate && 
    pip install -r requirements.txt
    ```

Install `geckodriver`

- Windows:

  - Download latest `geckodriver.exe` from [here](https://github.com/mozilla/geckodriver/releases/).
  - Unzip and move / copy `geckodriver.exe` into your `venv\Scripts\` folder.

- Linux / MacOS:

  - Download latest `geckodriver` from [here](https://github.com/mozilla/geckodriver/releases/).
  - Untar and move / copy `geckodriver` into your `/usr/bin` or any other directory inside `PATH`.

## Usage

Always use `virtualenv` when interacting with these modules

- Windows:

  ```
  venv\Scripts\activate
  ```

- Linux / MacOS:

  ```bash
  . venv/bin/activate
  ```

### Run on terminal

```
python -m datagundar
```

### As a python module

`datagundar` has multiple modules, each modules will create a new _headless proxy_ of it's own. And each modules are a Class inherited from the `Proxy` Class.

```python
from datagundar import Jadwal
from datagundar import SAP
from datagundar import Vclass

Jadwal.getJadwalKelas(kelas)
# returns a dictionary of jadwal for selected kelas

# Data Structure:
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

# Data Structure:
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

# Data Structure:
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

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[GNU GPLv3.0](https://github.com/Rayhanga/DataGundar/blob/master/LICENSE)
