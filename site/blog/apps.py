from django.apps import AppConfig
from django.db.models.signals import post_migrate


class BlogConfig(AppConfig):
	name = 'blog'

	def ready(self):
		# post_migrate.connect(create_default_db, self)
		pass