from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class appgroup(models.Model):
    appgroup = models.CharField(max_length=50)
    appname = models.CharField(max_length=50)
    warpath = models.CharField(max_length=200)
    deploytype = models.CharField(max_length=10,default='jenkins')
    def __unicode__(self):
        return self.appgroup+self.appname
class apphost(models.Model):
    hostaddr = models.CharField(max_length=30)
    username = models.CharField(max_length=20,default='root')
    path = models.CharField(max_length=200)
    appgroup = models.ForeignKey(appgroup)
    def __unicode__(self):
        return self.hostaddr
class auth(models.Model):
    user = models.ForeignKey(User)
    appgroup = models.ForeignKey(appgroup)
class tasklog(models.Model):
    task_serial = models.CharField(max_length=20)
    task_host = models.CharField(max_length=30)
    begin_time = models.DateTimeField()
    end_time = models.DateTimeField()
    result = models.BooleanField()
    excute_user = models.ForeignKey(User)
    appgroup = models.ForeignKey(appgroup)
    log_type = models.CharField(max_length=10)
