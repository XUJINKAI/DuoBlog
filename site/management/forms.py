from django import forms
from django.conf import settings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import InlineCheckboxes

import os
from blog import models
from accounts import models as accounts_models


class BlogForm(forms.ModelForm):
	@staticmethod
	def get_themes():
		theme_dir = os.path.join(settings.BASE_DIR, 'templates', 'themes')
		r = []
		for dirname, dirnames, filenames in os.walk(theme_dir):
			for subdirname in dirnames:
				r.append([subdirname, subdirname])
		return r

	class Meta:
		model = models.Blog
		fields = '__all__'
		exclude = ['navs', 'posts_url_prefix', 'pages_url_prefix']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-md-4'
		self.helper.field_class = 'col-md-8'
		self.fields['theme'] = forms.ChoiceField(choices=self.get_themes())
		self.helper.add_input(Submit('submit', 'Save'))


class PageForm(forms.ModelForm):

	class Meta:
		model = models.Page
		fields = '__all__'