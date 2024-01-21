from django.contrib.auth.base_user import AbstractBaseUser
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractBaseUser):
	name = models.CharField(max_length=150)
	is_active = models.BooleanField(default=True)
	is_superuser = models.BooleanField(default=False)
	is_staff = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.name}'