# RESTwitter

## Requirements

Python3 with pip

### Python requirements

```
$ pip install -r requirements.txt
```

## App Structure 

```
./
./django/restwitter
  ./restwitter            # settings and urls
  ./app                   # main app with models, views and unit tests
```

## DB Migrations

To generate migration please execute
```
$ python3 manage.py makemigrations
```

To run migrations please execute
```
$ python3 manage.py migrate
```

To run tests please execute
```
$ python3 manage.py test
```

To start web app please execute
```
$ python3 manage.py runserver <desired_interface_ip:desired_port>
```
