import os, sys
from random import choice
from string import ascii_lowercase, digits
from django.contrib.auth.models import User


from blog.models import Post



def get_conf_dict(path):
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

	domain_names = ['@ukr.net', '@gmail.com']
	for i in numb_users:
		username = ''.join(choice(ascii_lowercase), k=choice(range(min_len, max_len)))
		email = username + choice(domain_names)
		password = ''.join(choice(ascii_lowercase + digits, k=choice(range(min_len, max_len))))
		# user = User.objects.create_user(username=username,
		# 							    email=email,
		# 							    password1=password,
		# 							    password2=password)
		print(username, password, email)
		#return user





conf_path = 'config.conf'
conf = get_conf_dict(conf_path)
	# actions = {'singup': singup,
	# 		   'add_posts': add_posts,
	# 		   'add_likes': add_likes}

print(conf)

singup(conf['number_of_users'])