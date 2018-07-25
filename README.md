## BlogRestApi

``BlogRestApi`` is a simple Rest Api Blog.


### Basic functions:
* user singup
* user login
* post like
* post unlike

### Getting Started

1. Clone project:
```
> git clone https://github.com/Smidels/BlogRestApi.git
```
2. Crecte virtual environment:
```
> cd BlogRestApi
> python -m venv venv
```
3. Install requirements:
```
> pip install -r requirements.txt
(venv)>python manage.py runserver
```

### Usege Blog API

#### You can use httpie for HTTP requests. To do this, install httpie (you must use another termonal):
```
>pip install httpie
```
#### Registration user:
```
>http POST http://127.0.0.1:8000/rest-auth/registration/ 
```