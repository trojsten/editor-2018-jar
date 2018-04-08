## Django

First, best thing to do is create virtualenv.

Second, install Python project requirements

```
pip install -r requirements.txt
```

Run Django database migrations.

```
python manage.py migrate
```

To copy CKEditor run: `python manage.py collectstatic`.

Create admin user:

```
python manage.py createsuperuser
```

And finally, run server:

```
python manage.py runserver 0.0.0.0:8000
```

### How to access the local Django webserver from outside world

* what is your IP address? (`ipconfig`)
* add your IP to `ALLOWED_HOSTS` in `settings.py`
