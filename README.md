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
2. Create virtual environment:
```
> cd BlogRestApi
> python -m venv venv
```
3. Install requirements:
```
> pip install -r requirements.txt
```
4. Run our server:
```
(venv)>python manage.py runserver
```

#### You can use httpie for HTTP requests. To do this, install httpie (you must use another terminal):
```
>pip install httpie
```

### Usage Blog API


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
#### Delete post:
```
>http -a you_nickname:you_password123 DELETE http://127.0.0.1:8000/posts/4/
```
> Note: you can delete only your post

#### Like post:
```
>http -a you_nickname:you_password123 http://127.0.0.1:8000/like/ post=3
```
> 3 it is id_post

#### Unlike post:
```
>http -a you_nickname:you_password123 http://127.0.0.1:8000/unlike/ post=3
```

### Usage bot

When you start the bot, it reads the data from config/config.conf.
Example config.conf:
```
number_of_users:2
max_posts_per_user:4
max_likes_per_user:6
```
> Other key values no need to be included!

If config file is valid, bot register users, and create posts on their behalf. Likes are generated from an accidental user.

#### Run bot:
```
http http://127.0.0.1:8000/bot/ run=True
```
