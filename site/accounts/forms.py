from django import forms
import django.contrib.auth.forms as auth_form
from . import models

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions


class CreateSuperUserForm(auth_form.UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta(auth_form.UserCreationForm.Meta):
		model = models.User