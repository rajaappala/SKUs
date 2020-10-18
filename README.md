# SKU

### API
### Installation
```
* python3 -m venv env
* source env/bin/activate
* pip install -r requirements.txt
```

### Export following variables

```
* export DEBUG=1
* export SECRET_KEY=your secret key
* export SQL_ENGINE=django.db.backends.mysql
* export SQL_DATABASE=your db name
* export SQL_USER=your db user
* export SQL_PASSWORD=your password
* export SQL_HOST=localhost
* export SQL_PORT=3306
```

### Export running
```
* python manage.py migrate
* python manage.py runserver
```

Create superuser to access the api using following command
* python manage.py createsuperuser


### UI
* use node version 12.19.0
```
* npm install
* npm run serve
```


## Running the application with docker
```
* docker-compose build
* docker-compose up
```

Create superuser to access the api using following command
* python manage.py createsuperuser