# Directorx
## Heroku Deployment

https://directox.herokuapp.com/

## Getting Started

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by naviging to the `/DirectorX` directory and running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/) is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py.

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server.

## Database Setup

With Postgres running, restore a database using the casting_agency.psql file provided. From the backend folder in terminal run:

```
python db upgrade
```

## Running the server

From within the `starter` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
setup.sh
flask run
```

To run the server for test, execute:

```bash
test_runner.sh
```

## API Reference
### Getting started
- Base URL: The app can only be run locally as it has not been hosted as a base url. The backend is hosted at ```http://127.0.0.1:5000```.

### Error Handling
Errors are return as JSON objects in the following format
```
{
    "success": False,
    "error": 400,
    "message": 'bad request'
}
```
The endpoints will return three types of errors when request fails;
- 400: Bad request
- 404: Resource Not found
- 422: unprocessable

### Endpoints
```
GET '/movies'
GET '/actors'
POST '/movies'
POST '/actors'
PATCH '/movies/<int:id>'
PATCH '/actors/<int:id>'
DELETE '/movies/<int:id>'
DELETE '/actors/<int:id>'
```

GET '/movies'
- Fetches a list of dictionaries of movies which contains key-value pairs of information about the movies
- Request Arguments: None
- Returns: A list of movie dictionaries

- Sample: ```curl http://127.0.0.1:5000/movies```
```
{
    success: True,
    movies: [{title:'Hancock',release_date:'2019-20-20'},
            {title:'lion',release_date:'2017-10-18'}
            {title:Incredibles',release_date:'2018-05-15'}]
}

```

GET '/actors'
- Fetches a list of dictionaries of actors which contains key-value pairs of information about the actors
- Request Arguments: None
- Returns: A list of actor dictionaries

- Sample: ```curl http://127.0.0.1:5000/actors```
```
{
    'success': True,
    'actors': [{
        'id': 1,
        'name':'Terrance howard'
        'age': 24
    },
        'id': 2,
        'name':'Jessie smallet'
        'age': 29
    }],
}
```

DELETE '/actors/<int:id>'
- Deletes a particular actor
- Request Argument: id
- Returns: An object with keys;
     success: True
     delete: the id of deleted question.
- Sample: ```curl -X DELETE http://127.0.0.1:5000/actors/1```
```
{
    'success': True,
    'delete': 1,
}
```

DELETE '/movies/<int:id>'
- Deletes a particular movies
- Request Argument: id
- Returns: An object with keys;
     success: True
     delete: the id of deleted movie.
- Sample: ```curl -X DELETE http://127.0.0.1:5000/actors/1```
```
{
    'success': True,
    'delete': 1,
}

```
POST '/movies'
- creates a new movie.  
- Request Argument: None
- Returns: An object with keys;
     id: the id of newly created question.
     title: the title of the movie.
     release_date.
- Sample: ```curl http://127.0.0.1:5000/movies -X POST -H "Content-type: application/json" -d '{"title": 'bottle neck', "release_date": '2013-07-23}'```
```
{
    'success': True,
    'movie': {
        'id': 1,
        'title': 'bottleneck';
        'release_date: '2018-12-06
    }
}
```
```


```

POST '/actors'
- creates a new actor.  
- Request Argument: None
- Returns: An object with keys;
     id: the id of newly created question.
     name: the title of the movie.
     age:56
     gender: male
- Sample: ```curl http://127.0.0.1:5000/actors -X POST -H "Content-type: application/json" -d '{"name": 'tunde ednut', "age":34, gender:"male"}'```
```
{
    'success': True,
    'actor': {
        'id': 1,
        "name": "tunde".
        "age":56
        "gender": "male"
    }
}
```

PATCH '/actors/<int:id>'
- updates actor details 
- Request Argument: None
- Returns: An object with keys;
     id: the id of newly created question.
     name: the title of the movie.
     age:56
     gender: male
- Sample: ```curl http://127.0.0.1:5000/actors -X PATCH -H "Content-type: application/json" -d '{"name": 'sogi ednut'}'```
```
{
    'success': True,
    'actor': {
        'id': 1,
        "name": "tunde".
        "age":56
        "gender": "male"
    }
}

```

PATCH '/movies/<int:id>'
- updates amovie details 
- Request Argument: None
- Returns: An object with keys;
     id: the id of newly created question.
     title: the title of movie
     release_date
- Sample: ```curl http://127.0.0.1:5000/movies -X PATCH -H "Content-type: application/json" -d '{"title": 'neck ednut'}'```
```
{
    'success': True,
    'movie': {
        'id': 1,
        'title': 'neck';
        'release_date': '2018-12-06'
    }
}
```

## Testing
To run the tests, run
```
bash test_runner.sh
```