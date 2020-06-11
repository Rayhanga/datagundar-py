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

### As a CLI

```
python -m datagundar
```

### As a REST API server:

To startup the development server use:

```
python -m restapi
```

For production server use `gunicorn` or any other WSGI.

```bash
# Example deployment with gunicorn
gunicorn restapi:app
```

For more documentation on available API please refer to [`restapi` README.md](https://github.com/Rayhanga/DataGundar/blob/master/restapi/README.md)

### As a python module

Please refer to [`datagundar` README.md](https://github.com/Rayhanga/DataGundar/blob/master/datagundar/README.md)

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[GNU GPLv3.0](https://github.com/Rayhanga/DataGundar/blob/master/LICENSE)
