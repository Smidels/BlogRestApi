import requests
import time
import os, sys
from random import choice
from string import ascii_lowercase, digits

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import status

from blog.models import Post
from blog.serializers import PostSerializer, UserSerializer
from blog.permissions import IsOwnerOrReadOnly




class UserViewSet(viewsets.ReadOnlyModelViewSet):

	"""
	This viewset automatically provides 'list and 'detail' actions for User model.
	"""

	queryset = User.objects.all().order_by('id')
	serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):

	"""
	This viewset automatically provides 'list and 'detail' actions for Post model.
	"""

	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
		IsOwnerOrReadOnly, )

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)



@api_view(['GET'])
def api_root(request, format=None):
	
	"""
	List all models in root ulr
	"""

	return Response({
		'users': reverse('user-list', request=request, format=format),
		'posts': reverse('post-list', request=request, format=format)
		})



@api_view(['POST'])
def like(request):

	"""
	Like to the post object
	"""
	
	if request.user.is_anonymous:
		return Response(status=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)

	elif request.method == 'POST':
		user = request.user
		user_id = user.id
		post_id = request.data['post']
		post = Post.objects.get(id=post_id)
		post.votes.up(user_id)
		return Response({'User {} like post: {}.'.format(user.username, post.text)}, status=status.HTTP_200_OK)


@api_view(['POST'])
def unlike(request):
	
	"""
	Unlike to the post object if you've been like this post
	"""
	
	if request.user.is_anonymous:
		return Response(status=status.HTTP_511_NETWORK_AUTHENTICATION_REQUIRED)

	elif request.method == 'POST':
		user = request.user
		user_id = user.id
		post_id = request.data['post']
		post = Post.objects.get(id=post_id)
		post.votes.down(user_id)
		return Response({'User {} unlike post: {}.'.format(user.username, post.text)}, status=status.HTTP_200_OK)




@api_view(['POST'])
def run_bot(request):

	"""
	Launch bot
	"""
	start_time = time.time()
	message = {"Config file can't be read!"}
	if request.data['run'] == "True":
		conf = get_conf_dict()

		try:
			keys = ['number_of_users', 'max_posts_per_user', 'max_likes_per_user']

			for key in conf:
				if conf[key] < 1:
					return Response({'Numbers must be greates than zero'})
		except:
			return Response(message)

		users_data = singup(conf['number_of_users'])
		posts_id = posts_generator(conf['max_posts_per_user'], users_data)
		likes_generator(conf['max_likes_per_user'], posts_id)

	else:
		return Response({'To start the bot, you must enter run=True'},
		 				status=status.HTTP_400_BAD_REQUEST)
	finish_time = time.time()
	timer = int(finish_time - start_time)
	timer = 'Spend time {} c.'.format(timer)
	print(timer)
	return Response({timer}, status=status.HTTP_201_CREATED)


def get_conf_dict():

	"""
	Reading config file and create dict with info
	"""

	path_to_conf = os.path.join(os.path.dirname(
								os.path.dirname(__file__)),
								'blog\\config\\config.conf'
								)

	try:
		with open(path_to_conf, 'r') as f:
			lines = [i for i in f.read().split('\n') if i != '']

			create_action = [i.split(':')[0] for i in lines]
			value = [int(i.split(':')[1]) for i in lines]
	except:
		return Response()
	conf_dict = dict(zip(create_action, value))

	return conf_dict
	


def singup(num_users):

	"""
	Automaticaly registers users
	"""

	min_len = 8
	max_len = 16

	domain_names = ['@ukr.net', '@gmail.com']
	users_data = {}
	for i in range(num_users):

		username = ''
		len_username = choice(range(min_len, max_len))

		for _ in range(len_username):
			username += choice(ascii_lowercase)
		email = username + choice(domain_names)
		password = ''

		for _ in range(min_len, max_len):
			password += choice(ascii_lowercase + digits)

		try:
			user = User.objects.create_user(username=username,
									    email=email,
									    password=password
									    )
		except:
			print('Could not register "{}"'.format(username))
			continue
		
		users_data[i] = {'username': username,
						 'password': password}
		print('Register {}, password={}, email={}'.format(
														  username,
														  password,
														  email
														  ))
	return users_data


def get_random_text():

	"""
	Generate random text
	"""

	max_word = 10
	word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
	response = requests.get(word_site)
	words = response.content.splitlines()
	post = ''

	for i in range(max_word):
		post += choice(words).decode("utf-8") + ' '
	post.capitalize()
	return post



def posts_generator(max_num_posts, users_data):

	"""
	Add posts from users
	"""
	posts_id = []
	for i in users_data:
		try:
			username = users_data[i]['username']
			password = users_data[i]['password']
			user = User.objects.get(username=username)
		except:
			return Response({'User "{}"'.format(username): ' not found'})
			break

		num_posts = choice(range(max_num_posts))

		for _ in range(num_posts):
			text = get_random_text()
			post = Post(text=text, owner=user)
			post.save()
			posts_id.append(post.id)
			print('User {} add post {}'.format(username, post))
	return posts_id


def likes_generator(max_num_likes, posts_id):

	"""
	Add like to posts
	"""

	users_id = User.objects.values_list('id')
	if max_num_likes > len(users_id):
		max_num_likes = len(users_id)
		
	for post_id in posts_id:
		num_likes = choice(range(max_num_likes))
		post = Post.objects.get(id=post_id)

		while True:
			if post.votes.count() == num_likes:
				break

			user_id = choice(users_id)[0]
			post = Post.objects.get(id=post_id)
			post.votes.up(user_id)
			username = User.objects.get(id=user_id).username
			print('User "{}"" like "{}"'.format(username, post.text))
	