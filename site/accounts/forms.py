from django import forms
import django.contrib.auth.forms as auth_form
from . import models

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Div, Submit, HTML, Button, Row, Field
from crispy_forms.bootstrap import AppendedText, PrependedText, FormActions

from allauth.account import forms as allauth_forms


class LoginForm(allauth_forms.LoginForm):
	email = forms.EmailField(required=False)

	class Meta(auth_form.UserCreationForm.Meta):
		model = models.User


class SignupForm(auth_form.UserCreationForm):
	email = forms.EmailField(required=False)

	class Meta(auth_form.UserCreationForm.Meta):
		model = models.User


class CreateSuperUserForm(auth_form.UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta(auth_form.UserCreationForm.Meta):
		model = models.User


class UserForm(forms.ModelForm):

	class Meta:
		model = models.User
		fields = ['username', 'first_name', 'last_name', 'email']