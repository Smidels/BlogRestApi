from django.db import models
from vote.models import VoteModel


class Post(VoteModel, models.Model):
	created = models.DateTimeField(auto_now_add=True)
	text = models.TextField()

	owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)

	class Meta:
		ordering = ('created', )
