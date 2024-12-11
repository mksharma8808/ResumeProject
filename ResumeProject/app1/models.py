from django.db import models

# Create your models here.

class Users(models.Model):
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=20)

class Resumes(models.Model):
    # resume = models.CharField(max_length=255)
    ruid = models.ForeignKey(Users,on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes')