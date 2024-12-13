from django.db import models
from datetime import datetime
# Create your models here.

class Users(models.Model):
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=20)

class Resumes(models.Model):
    ruid = models.ForeignKey(Users,on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes')
    created_at_time = models.DateTimeField(auto_now_add=True,null=True)