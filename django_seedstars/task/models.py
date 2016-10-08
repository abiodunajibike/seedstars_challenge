from django.db import models
#from django.contrib.auth.models import User


# class UserInfo(User):
#     
#     def __unicode__(self):
#         return "%s - %s" %(self.get_full_name(), self.email)

class UserInfo(models.Model):
    name        =  models.CharField(max_length = 100)
    email       =  models.EmailField()

    def __unicode__(self):
        return "%s - %s" %(self.name, self.email)
