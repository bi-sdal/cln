from django.http import HttpResponseRedirect
from django.contrib.auth.views import login
from django.shortcuts import render

def login_redirect(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('projects')
    else:
        return login(request)
        