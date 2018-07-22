from django.contrib.auth.models import User
from rest_framework import serializers
#from rest_framework.decorators import api_view
from blog.models import Post


class PostSerializer(serializers.HyperlinkedModelSerializer):
	owner = serializers.ReadOnlyField(source='owner.username')
	
	votes = serializers.ReadOnlyField(source='votes.count')

	class Meta:
		model = Post
		fields = ('url', 'owner', 'id', 'text', 'votes')




class UserSerializer(serializers.HyperlinkedModelSerializer):
	posts = serializers.HyperlinkedRelatedField(many=True, view_name='post-detail', read_only=True)
	
	class Meta:
		model = User
		fields = ('url', 'id', 'username', 'posts')


