# Rates Task

This project includes my solution for the Xeneta technical task. The project is built with Flask and PostgreSQL, and it uses Poetry for dependency management.

## Project Structure

The structure of the repository is as follows:

```plaintext
ratestask/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── queries.py
│   ├── routes.py
│   ├── config.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py
│   │   └── helpers.py
│   └── services/
│       ├── __init__.py
│       └── rates_service.py
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_rates_api.py
│   ├── test_setup.py
│   └── test_validators.py
│
├── rates.sql
├── Dockerfile
├── Dockerfile.flask
├── docker-compose.yml
├── pyproject.toml
├── poetry.lock
└── README.md
```

## Setup

There are generally two ways you can access the application:

### Docker Compose

1. Clone the repository and go inside the `ratetask` folder:

```
git clone https://github.com/yourusername/ratestask.git && cd ratestask
```

2. Next up, run the following command:

```
docker-compose up --build
```

This basically will:

* Build the Flask app image, starting the server on port 5000
* Build the PostgreSQL image and initialize the database with `rates.sql` on port 5432
* Run all the tests associated with the API

You can then access the flask server through the `http://127.0.0.1:5000` or `http://0.0.0.0:5000` url.

### Without Docker Compose

For this, we would first need to setup our database and then run the flask application manually.

---

#### Database setup:

We can use the provided Dockerfile to start the PostgreSQL instance populated with the assignment data. You can execute the provided Dockerfile by running:

```bash
docker build -t ratestask .
```

This will create a container with the name *ratestask*, which you can start in the following way:

```bash
docker run -p 0.0.0.0:5432:5432 --name ratestask ratestask
```

You can connect to the exposed Postgres instance on the Docker host IP address, usually *127.0.0.1* or *172.17.0.1*. It is started with the default user `postgres` and `ratestask` password.

```bash
PGPASSWORD=ratestask psql -h 127.0.0.1 -U postgres
```

alternatively, use `docker exec` if you do not have `psql` installed:

```bash
docker exec -e PGPASSWORD=ratestask -it ratestask psql -U postgres
```

Keep in mind that any data written in the Docker container will disappear when it shuts down. The next time you run it, it will start with a clean state.

---

#### Application Setup:

To setup your application, you need to first have `poetry` installed. If it isn't, you can do so by running the follwoing command:

```
pip install poetry
```

Next, we need to install all our dependencies:

```
poetry install
```

You can then run the following command to start your flask application:

```
poetry run flask run    
```

If you're on Linux or Mac, you can also use `gunicorn` to start your app:

```
poetry run gunicorn --bind 0.0.0.0:5000 app.main:app
```

You can now access the application through the following url:

```
http://0.0.0.0:5000/
```

You can also execute the following command to run the tests:

```
pytest
```
