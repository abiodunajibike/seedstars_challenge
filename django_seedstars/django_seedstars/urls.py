
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from task import views

urlpatterns = [    
    url(r'^$', TemplateView.as_view(template_name = 'task/index.html'), name="index"),
    url(r'^add/$', views.UserInfoCreate.as_view(), name="add_user"),
    url(r'^list/$', views.UserList.as_view(), name="user_list"),
    url(r'^admin/', include(admin.site.urls)),

]



