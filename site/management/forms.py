from django import forms
from django.conf import settings
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Submit
from crispy_forms.bootstrap import InlineCheckboxes

from django.contrib.sites.models import Site
from django.contrib.flatpages.models import FlatPage
from blog import models
from accounts import models as accounts_models


class BlogForm(forms.ModelForm):

	class Meta:
		model = models.Blog
		fields = '__all__'
		exclude = ['site', 'posts_url_prefix', 'pages_url_prefix']

	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.helper = FormHelper(self)
		self.helper.form_class = 'form-horizontal'
		self.helper.label_class = 'col-md-4'
		self.helper.field_class = 'col-md-8'
		self.helper.add_input(Submit('submit', 'Save'))