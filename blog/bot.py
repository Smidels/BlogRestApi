import os, sys
from random import choice
from string import ascii_lowercase, digits

#from django.contrib.auth.models import User

from blog.models import Post



def get_conf_dict():
	path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'blog\\config\\c')
	with open(path, 'r') as f:
		lines = [i for i in f.read().split('\n') if i != '']
		print('lines', lines)

		create_action = [i.split(':')[0] for i in lines]
		print(create_action)

		value = [int(i.split(':')[1]) for i in lines]
		print(value)
		conf_dict = dict(zip(create_action, value))
	return conf_dict


def singup(numb_users):
	min_len = 8
	max_len = 16
	new_users = []
	domain_names = ['@ukr.net', '@gmail.com']
	for i in range(numb_users):
		username = ''
		for i in range(min_len,max_len):
			username += choice(ascii_lowercase)

		email = username + choice(domain_names)

		password = ''
		for i in range(min_len, max_len):
			password += choice(ascii_lowercase + digits)
		# user = User.objects.create_user(username=username,
		# 							    email=email,
		# 							    password1=password,
		# 							    password2=password)

		new_users.append(username)
	return new_users