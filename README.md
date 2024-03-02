# Seun Dawodu tech task for Edgefolio
## Notes

### Set up

- install requirements
```
pip install -r requirements.txt
```

- create db
```
python manage.py migrate
```

- create superuser
```
python manage.py createsuperuser
```

- start webserver
```
python manage.py runserver
```

- to start interactive shell
```
python manage.py shell_plus
```

### Fund list page/API end point
Visit http://127.0.0.1:8000/funds/funds/ from browser to view HTML list page.
A cURL (or similar) request to the same end point will return a JSON payload
```
curl http://127.0.0.1:8000/funds/funds/
```
This endpoint supports filtering by `strategy` using a querystring parameter

A detail end point for each fund by primary key exists at 
http://127.0.0.1:8000/funds/funds/<pk>/

### csv upload
CSV uploads are only supported via the django admin, so a superuser will need to be created


## To Do
- Implement dropdown filtering on HTML list page
- Django web page upload of file imports
- file import status reporting
- Asynchronous processing of CSV imports so that users are not left waiting for response from backend on large uploads using something like celery
- Containerise the application (to make async processing tidy)
