
from models import UserInfo

from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import CreateView
from django.views.generic.list import ListView
from django.contrib.messages.views import SuccessMessageMixin


class UserInfoCreate(SuccessMessageMixin, CreateView):
    model           = UserInfo
    fields          = '__all__'
    '''I needed to use reverse_lazy in place of reverse because of exceptions.ImproperlyConfigured'''
    success_url     = reverse_lazy('user_list')
    success_message = 'User record successfully added'
    

class UserList(ListView):
    model            = UserInfo
    
