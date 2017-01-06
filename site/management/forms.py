from django import forms
from django.conf import settings
from blog import models
from accounts import models as accounts_models


class BlogForm(forms.ModelForm):
	
	class Meta:
		model = models.Blog
		fields = '__all__'


class UserForm(forms.ModelForm):

	class Meta:
		model = accounts_models.User
		fields = '__all__'