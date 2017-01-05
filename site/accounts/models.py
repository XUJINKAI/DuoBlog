from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.sites.models import Site

# Create your models here.


class User(AbstractUser):
	site = models.ForeignKey(Site)