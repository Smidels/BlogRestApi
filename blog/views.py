import os, sys
from random import choice
from string import ascii_lowercase, digits
import requests

from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse


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
		return Response({'anonymous user': "can't like or unlike"})

	elif request.method == 'POST':
		user_id = request.user.id
		post_id = request.data['post']
		post = Post.objects.get(id=post_id)
		post.votes.up(user_id)
		return Response({'you like': post.text})


@api_view(['POST'])
def unlike(request):
	
	"""
	Unlike to the post object if you've been like this post
	"""
	
	if request.user.is_anonymous:
		return Response({'anonymous user': "can't like or unlike"})

	elif request.method == 'POST':
		user_id = request.user.id
		post_id = request.data['post']
		post = Post.objects.get(id=post_id)
		post.votes.down(user_id)
		return Response({'you unlike': post.text})


@api_view(['POST'])
def run_bot(request):

	"""
	Launch bot
	"""

	if request.data['bot'] == 'run':
		conf = get_conf_dict()

	# actions = {'singup': singup,
	# 		   'add_posts': add_posts,
	# 		   'add_likes': add_likes}

		users = singup(conf['number_of_users'])

		return Response(users)


def get_conf_dict():

	"""
	Reading config file and create dict with info
	"""

	path_to_conf = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'blog\\config\\config.conf')
	with open(path_to_conf, 'r') as f:
		lines = [i for i in f.read().split('\n') if i != '']
		create_action = [i.split(':')[0] for i in lines]
		value = [int(i.split(':')[1]) for i in lines]
		conf_dict = dict(zip(create_action, value))
	return conf_dict


def singup(numb_users):

	"""
	Automaticaly registers users
	"""

	min_len = 8
	max_len = 20

	domain_names = ['@ukr.net', '@gmail.com']
	users_data = {}
	for i in range(numb_users):
		# Generation username, password and email.

		username = ''
		len_username = choice(range(min_len, max_len))
		for i in range(len_username):
			username += choice(ascii_lowercase)

		email = username + choice(domain_names)

		password = ''
		for i in range(min_len, max_len):
			password += choice(ascii_lowercase + digits)
		user = User.objects.create_user(username=username,
									    email=email,
									    password=password
									    )
		users_data[i] = {username: password}
		print('Register {}, password={}, email={}'.format(username, password, email))
	return users_data


def gener_posts(numb_posts, users_data):

	"""
	Generation posts for all users
	"""

	max_word = 5
	word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
	response = requests.get(word_site)
	words = response.content.splitlines()
	post = ''
	for i in max_word:
		post += choice(words)
	#post.capitalize() += '.'

