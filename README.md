# Core Notification API

application for notification service

author: ekoabdulaziz96@gmail.com

## Prerequisites

[![Code](https://img.shields.io/badge/Code-Python-1B9D73?style=flat&logo=python)](https://python.org)
[![Framework](https://img.shields.io/badge/Framework-Flask-1B9D73?style=flat&logo=flask)](https://flask.palletsprojects.com/)
[![Ruff](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/ruff/main/assets/badge/v2.json)](https://github.com/astral-sh/ruff)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

## How to run
Make sure you already installed **python3.10** or higher in your machine

1. Create your virtualenv and activate (if you are using virtuanenv)
2. Install library 
    ```sh
    # for development purpose
    pip install -r ./requirements/dev.txt

    # for production server
    pip install -r requirements.txt
    ```
3. Move your current root path to this project
    ```sh
    cd core-notification-api
    ```
4. make .env file, you can duplicate it from .env.dev and rename it to .env
    - you can edit the value for your own environment IP/port or something else
    - recommend to use same environment with author, we use docker that inclue `PostgreSQL, Adminer, Redis`
    - step to run container docker
        ```sh
        # change directory to xsources
        cd xsources

        # run docker compose
        docker-compose -f .\postgres_redis.yml up -d
        ```
    - step to turn off container docker
        ```sh
        # turn off docker compose
        docker-compose -f .\postgres_redis.yml down
        ```
    - make sure the DB is already created, 
        - you can open adminer in your browser with url `http://localhost:8080/`
        - login with credential:
            - sistem = PostgreSQL
            - server = postgresDocker
            - pengguna = postgres
            - sandi = postgres
        - check the the DB `db_core_notification` is exist or not, 
            - you can create it, if not exist
    - make sure your .env file is corrent value
        - FLASK_ENV : value ['development', 'staging', 'production']
        - MAIL_* value, if you want to change it make sure your account 2 step auth and generate your app password

    
5. run migraton file
    ```sh
    flask db upgrade -d 'models/migrations'
    ```
6. seed data in DB
    ```sh
    # make sure, you are in the root project
    # seed data user recipient
    python .\seeders\emails.py
    ```
7. run server flask
    ```sh
    # make sure, you are in the root project
    flask run
    ```
8. run server celery worker
    ```sh
    # create new terminal and activate the virtualenv
    # make sure, you are in the root project
    
    # celery worker
    celery -A server.celery worker --loglevel INFO

    # celery worker on windows user, `--pool solo`
    celery -A server.celery worker --pool solo --loglevel INFO
    ```

9. run server celery beat (scheduler)
    ```sh
    # create new terminal and activate the virtualenv
    # make sure, you are in the root project
    # caution, please run celery worker first

    # celery beat
    celery -A server.celery beat --loglevel INFO
    ```

### Need to know
- you can set your `TIMEZONE`, and `TIMEZONE_ADD_HOUR_FROM_UTC` in .env file
- you can set your email threshold (`EMAIL_TIMESTAMP_THRESHOLD`) in env file, you can set it to `0` minutes
-  

<br>

### How to set connection DB
Set your .env file for variable key for `SQLALCHEMY_DATABASE_URI` 
<br> ex : `SQLALCHEMY_DATABASE_URIL="postgresql://username:password@host:port/db_name"`
<br><br>

### How to Manage ORM DB 
1. only for the first time, when you create migration file
    ``` sh
    flask db init -d 'models/migrations'
    ```

2. Create your ORM class for table in `./models/your_table_names.py`
3. Register your new ORM class (new table) in .`/models/_register_tables.py`
    <br>if your new ORM class is not registered yet, you cann't migrate your db

4. make migrate file (alembic), for any change in your models
    ``` sh
    flask db migrate -d 'models/migrations' -m 'custom_message'
    ```
    re-check your migrate file in `./models/migrations/versions`, cz cannot detect rename table/column automatically.

5. execute migration for your change in db
    ``` sh
    flask db upgrade -d 'models/migrations'
    ```

<br>

### Unittest
all of unit test all saved in `./tests/*` folder. 

1. Run Unittest (using pytest)
<br>You can run unittest by executing this command 
    ``` sh
    # run all unittest
    pytest tests

    # run specific unittest
    # pytest tests/package/moduleName.py::className::functionName
    # ex:
    pytest tests/test_server.py::TestServer::test_case_1
    ```
2. Coverage
    ``` sh
    # run all test
    # you can skip module/file in .coveragerc file
    coverage run --source='.' --rcfile='.coveragerc' -m pytest

    # make report
    coverage report

    # make html report
    coverage html
    # follow the generated htmlcov path and open it in browser
    # ex: Wrote HTML report to `htmlcov\index.html`
    ```
<br>

### Lint & Format
Ruff re-implements some of the most popular Flake8 plugins and related code quality tools (include: isort)
```sh
#  LINTING
# check the code first
ruff check .

# auto fix 
ruff check --fix

# ignore check , add this comment after last code `# noqa`
# ex: a = 1   # noqa
```

Auto Formatter with black 
```sh
# check first
black --config .\pyproject.toml . --check

# run black
black --config .\pyproject.toml  app_name/sub_folder

# ignore check , add this comment after last code `# noqa`
# ex: a = 1   # fmt: skip
```
    
<br>


### Direktory explaination:
```sh
./constants         # place your static data, variable, etc 
./cores             # place for app, config, extension, core class : [middleare, response, etc]
./models            # place for ORM models and migration file 
__./migrations      # place migration file 
./modules           # place for bussiness logic, implement third party services, 
./requirements      # place for requirement (dev, prod)
./seeder            # place for seed data, init data, for aplication
./serializers       # place for serializer class
./tasks             # place for background task
./tests             # place for unittest
./urls              # place for url route
./views             # place for views / controller logic
./xsource           # place for documentation and important file for environment
.coveragerc         # setting data coverage
.pyproject.toml     # config pytest.ini and isort
server.py           # server app
requirements.txt    # requirement library python (for production only)
start-app.sh        # setting bash script to run app
```

<br>

### Note:
- this project is created base on [flask cookiecuter](https://github.com/cookiecutter-flask/cookiecutter-flask)
- structure module and name are insipired from [Django Rest Framework](https://www.django-rest-framework.org/)
- The goal is to build boilerplate/skeleton/template microservices project for RESTfull API
- author: ekoabdulaziz96@gmail.com
