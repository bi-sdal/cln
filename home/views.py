from django.http import HttpResponseRedirect
from django.contrib.auth.views import login
from django.contrib.auth.models import User
from django.shortcuts import render
from django.urls import reverse

from django.views.generic import UpdateView

def login_redirect(request):
    if request.user.is_authenticated and (request.user.last_login == None):
        return HttpResponseRedirect(reverse('update-profile', kwargs= {'pk': request.user.pk}))
    elif request.user.is_authenticated:
        return HttpResponseRedirect('projects')
    else:
        return login(request)
        

class UpdateProfile(UpdateView):
    model = User
    fields = ['first_name', 'last_name', 'email'] 
    template_name = 'registration/update_profile.html'
    
    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect('/projects/')