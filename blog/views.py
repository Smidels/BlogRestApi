from django.contrib.auth.models import User
from rest_framework import generics, permissions, renderers, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse

from blog.models import Post
from blog.serializers import PostSerializer, UserSerializer
from blog.permissions import IsOwnerOrReadOnly




class UserViewSet(viewsets.ReadOnlyModelViewSet):

	"""
	This viewset automatically provides 'list and 'detail actions.
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
