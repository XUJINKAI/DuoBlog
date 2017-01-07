from django.apps import AppConfig
from django.db.models.signals import post_migrate
from .management import create_default_db


class BlogConfig(AppConfig):
	name = 'blog'

	def ready(self):
		post_migrate.connect(create_default_db, self)