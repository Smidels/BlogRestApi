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

#### You can use httpie for HTTP requests. To do this, install httpie (you must use another termonal):
```
>pip install httpie
```

### Usege Blog API

#### Registration user:
```
>http http://127.0.0.1:8000/rest-auth/registration/ username=you_nickname email=you_email@gmail.com password1=you_password123 password2=you_password123 
```

#### Login:
```
>http http://127.0.0.1:8000/rest-auth/login/ username=you_nickname password=you_password123 
```
##### or
```
>http -a you_nickname:you_password123  http://127.0.0.1:8000/ 
```

#### Add post:
```
>http -a you_nickname:you_password123 http://127.0.0.1:8000/posts/ text="some text"
```

http://127.0.0.1:8000/rest-auth/like/

http://127.0.0.1:8000/rest-auth/unlike/

http://127.0.0.1:8000/rest-auth/bot/