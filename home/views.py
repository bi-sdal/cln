from django.http import HttpResponseRedirect
from django.contrib.auth.views import login
from django.contrib.auth.models import User
from django.shortcuts import render

from django.views.generic import UpdateView

def login_redirect(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('projects')
    else:
        return login(request)
        

class UpdateProfile(UpdateView):
    model = User
    fields = ['first_name', 'last_name'] 
    template_name = 'update_profile.html'