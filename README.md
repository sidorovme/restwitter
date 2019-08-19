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

To generate migration execute 
```
$ python3 manage.py makemigrations
```

To run migrations execute 
```
$ python3 manage.py migrate
```

To run tests execute
```
$ python3 manage.py test
```
