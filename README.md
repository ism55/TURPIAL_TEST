# Django-PostgreSQL Pokemon
<br/>

Test project for selection process

# Instructions

First, clone this repository with:

```
git clone https://github.com/ism55/TURPIAL_TEST.git
```
## PostgreSQL

### Windows
The easiest way to install Postgres on Windows is using a program you can find here: http://www.enterprisedb.com/products-services-training/pgdownload#windows

Choose the newest version available for your operating system. Download the installer, run it and then follow the instructions available here: http://www.postgresqltutorial.com/install-postgresql/.

## Database

Create a database [db_name] with postgresql user [postgre_user] and postgresql password [postgre_pass]

[db_host] is commonly 'localhost'

[db_port] normally 5432


Then, go to [django_turpial\settings.py](https://github.com/ism55/TURPIAL_TEST/blob/8c87bde7d2d29786b49ff0c669cb834d2fe002d0/project/env/django_turpial/settings.py#L80) and edit

```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': [db_name],
        'USER': [postgre_user],
        'PASSWORD': [postgre_pass],
        'HOST': [db_host],
        'PORT': [db_port],
    }
}

```

## Python

You need Python 3.7 which you find here: https://www.python.org/downloads/release/python-379/

Remember to install pip also and setup environment variables. 

Just in case, be sure you can run virtual python environments to run this project.

## Virtual environment

Go to terminal and locate in ```\env``` folder inside project directory. 

Then, activate virtual environment before doing any of the following steps by running:

```
.\Scripts\activate
```

To deactivate, just run in terminal

```
deactivate
```

## Python Dependencies

First, we need to setup Python dependencies. To do that you need to run in terminal:

```
pip install -r .\requirements\requirements.txt

```

## Database demo data

To create database tables, run:

```
python manage.py migrate
```


Then, to fill with some test data run:

For users:
```
python manage.py loaddata D:\TURPIAL_PRUEBA\project\env\users_data.json.gz
```

Or

```
python manage.py loaddata D:\TURPIAL_PRUEBA\project\env\users_data.json
```



For Pokemon data:
```
 python manage.py loaddata D:\TURPIAL_PRUEBA\project\env\pokemon_data.json.gz
 ```

Or

```
python manage.py loaddata D:\TURPIAL_PRUEBA\project\env\pokemon_data.json
```
