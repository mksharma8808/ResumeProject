from django.db import models
from datetime import datetime
import os
import shutil
# Create your models here.

class Users(models.Model):
    email = models.CharField(max_length=200)
    password = models.CharField(max_length=20)

class Resumes(models.Model):
    ruid = models.ForeignKey(Users,on_delete=models.CASCADE)
    resume = models.FileField(upload_to='resumes/')
    created_at_time = models.DateTimeField(auto_now_add=True,null=True)
    
    def delete(self, *args, **kwargs):
        file_path = self.resume.path
        folder_path = os.path.dirname(file_path)
        
        super().delete(*args, **kwargs)
        
        if os.path.isfile(file_path):
            os.remove(file_path)
        if os.path.isdir(folder_path) and not os.listdir(folder_path):
            shutil.rmtree(folder_path)