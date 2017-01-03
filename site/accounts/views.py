from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.views.generic.edit import FormView
from . import models
from . import forms
from django.contrib.auth import login as auth_login
from django.contrib.auth import REDIRECT_FIELD_NAME

# Create your views here.

def index_view(request):
	raise Http404


def login_view(request):

	if models.User.objects.count() == 0:
		return HttpResponseRedirect(reverse('account_createsuperuser')+'?'+request.META['QUERY_STRING'])
	return render(request, 'account/login.html')


def signup_view(request):
	if models.User.objects.count() == 0:
		return HttpResponseRedirect(reverse('account_createsuperuser'))
	# if request.method == 'POST':
	# 	form = forms.SignupForm(request.POST)
	# 	if form.is_valid():
	# 		data = form.cleaned_data
	# 		user = models.User.objects.


def createsuperuser_view(request):
	if models.User.objects.count() != 0:
		return HttpResponseRedirect(reverse('account_index'))
	elif request.method == 'POST':
		form = forms.CreateSuperUserForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			user = models.User.objects.create_superuser(\
				data['username'],\
				data['email'],\
				data['password1'] )
			auth_login(request, user)
			return HttpResponseRedirect(reverse('account_index'))
	else:
		form = forms.CreateSuperUserForm()
	return render(request, 'account/createsuperuser.html', {'form': form })