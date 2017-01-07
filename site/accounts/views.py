from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect, Http404

from django.views import generic
from django.views.generic.edit import FormView
from django.contrib.auth import login as auth_login

from allauth.account import views as allauth_views

from . import models
from . import forms

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

def index_view(request):
	raise Http404


class EmptyUsersCreateSuperUserMixin:
	def dispatch(self, request, *args, **kwargs):
		if models.User.objects.count() == 0:
			return HttpResponseRedirect(reverse('accounts_createsuperuser')+'?'+request.META['QUERY_STRING'])
		return super(EmptyUsersCreateSuperUserMixin, self).dispatch(request, *args, **kwargs)


class LoginView(EmptyUsersCreateSuperUserMixin, \
			allauth_views.LoginView):
	form_class = forms.LoginForm
	template_name = 'accounts/login.html'
	success_url = '/'

login_view = LoginView.as_view()



class SignupView(EmptyUsersCreateSuperUserMixin, \
			allauth_views.SignupView):
	form_class = forms.SignupForm
	template_name = 'accounts/signup.html'
	success_url = '/'

signup_view = SignupView.as_view()



class CreateSuperUserView(allauth_views.SignupView):
	form_class = forms.CreateSuperUserForm
	template_name = 'accounts/createsuperuser.html'
	success_url = '/'

	def dispatch(self, request, *args, **kwargs):
		'''only when user table is empty'''
		if models.User.objects.count() > 0:
			return HttpResponseRedirect(reverse('accounts_login'))
		return super(CreateSuperUserView, self).dispatch(request, *args, **kwargs)

	def form_valid(self, form):
		data = form.cleaned_data
		user = models.User.objects.create_superuser(\
			data['username'],\
			data['email'],\
			data['password1'] )
		auth_login(self.request, user)
		return HttpResponseRedirect(self.get_success_url())

createsuperuser_view = CreateSuperUserView.as_view()


###
# An example for function view, 
# but can't deal redirect query
###
# def createsuperuser_view(request):
# 	if models.User.objects.count() != 0:
# 		return HttpResponseRedirect(reverse('accounts_index'))
# 	elif request.method == 'POST':
# 		form = forms.CreateSuperUserForm(request.POST)
# 		if form.is_valid():
# 			data = form.cleaned_data
# 			user = models.User.objects.create_superuser(\
# 				data['username'],\
# 				data['email'],\
# 				data['password1'] )
# 			auth_login(request, user)
# 			return HttpResponseRedirect(reverse('accounts_index'))
# 	else:
# 		form = forms.CreateSuperUserForm()
# 	return render(request, 'accounts/createsuperuser.html', {'form': form })


class ProfileView(generic.FormView):
	template_name = 'accounts/profile.html'
	form_class = forms.UserForm

profile_view = ProfileView.as_view()
