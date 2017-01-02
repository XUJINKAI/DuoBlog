from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404
from django.views.generic.edit import FormView
from . import models
from . import forms

# Create your views here.
def index(request):
	return Http404()


def login(request):
	if models.User.objects.count() == 0:
		return HttpResponseRedirect(reverse('account_createsuperuser'))
	return render(request, 'account/login.html')


def createsuperuser(request):
	if models.User.objects.count() != 0:
		return HttpResponseRedirect(reverse('account_index'))
	elif request.method == 'POST':
		form = forms.CreateSuperUserForm(request.POST)
		if form.is_valid():
			data = form.cleaned_data
			models.User.objects.create_superuser(\
				data['username'],\
				data['email'],\
				data['password1'] )
			return HttpResponseRedirect(reverse('account_login'))
	else:
		form = forms.CreateSuperUserForm()
	return render(request, 'account/createsuperuser.html', {'form': form })