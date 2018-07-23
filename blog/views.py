from django.contrib.auth.models import User
from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from blog.models import Post
from blog.serializers import PostSerializer, UserSerializer
from blog.permissions import IsOwnerOrReadOnly

from blog import bot
#from bot import bot


class UserViewSet(viewsets.ReadOnlyModelViewSet):

	"""
	This viewset automatically provides 'list and 'detail' actions.
	"""

	queryset = User.objects.all()
	serializer_class = UserSerializer


class PostViewSet(viewsets.ModelViewSet):
	queryset = Post.objects.all()
	serializer_class = PostSerializer
	permission_classes = (permissions.IsAuthenticatedOrReadOnly,
		IsOwnerOrReadOnly, )

	def perform_create(self, serializer):
		serializer.save(owner=self.request.user)



@api_view(['GET'])
def api_root(request, format=None):
	return Response({
		'users': reverse('user-list', request=request, format=format),
		'posts': reverse('post-list', request=request, format=format)
		})



@api_view(['POST'])
def like(request):

	# Like to the object

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

	# Unlike to the object
	
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
	if request.data['bot'] == 'run':
		#return Response({'sdcsv'})
		conf = bot.get_conf_dict()
	# actions = {'singup': singup,
	# 		   'add_posts': add_posts,
	# 		   'add_likes': add_likes}
		users = bot.singup(conf['number_of_users'])
		return Response(users)