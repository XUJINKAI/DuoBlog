from django.db import models

# Create your models here.
class BlogSetting(models.Model):
	key = models.CharField(max_length=32, primary_key=True)
	value = models.CharField(max_length=64)

	def is_setup():
		return BlogSetting.objects.count() != 0