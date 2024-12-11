from django import template
from django.conf import settings
from app1.models import Users

register = template.Library()

@register.filter()
def useremail(id):
    try:
        user = Users.objects.get(id = id)
        return user.email.capitalize()
    except:
        return 'Everyone'
    
@register.filter()
def LoginCheck(id=False):
    if id:
        return True
    return False

@register.filter()
def imageFind(img):
    return f'{settings.BASE_DIR}/uploads/resumes/{img}'


import os
@register.filter
def basename(value):
    return os.path.basename(value)