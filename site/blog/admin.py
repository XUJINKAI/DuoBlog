from django.contrib import admin
from . import models

# Register your models here.
@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
	pass


@admin.register(models.Post)
class PostAdmin(admin.ModelAdmin):
	pass


@admin.register(models.Comment)
class PostAdmin(admin.ModelAdmin):
	pass


@admin.register(models.Tag)
class PostAdmin(admin.ModelAdmin):
	pass