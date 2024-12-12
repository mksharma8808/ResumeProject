from django import template
from django.conf import settings
from app1.models import Users

register = template.Library()


def callPathFile(path):
    filepath = path[1:]
    string = ''
    c = 0
    for i in range(len(filepath)):
        if filepath[i] in ('%','2','0'):
            c += 1
            if(c == 3):
                c = 0
                string += ' '
        else:
            if(c == 3):
                c = 0
                string += ' '
            else:
                string += filepath[i]
    return string

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
@register.filter()
def basename(value):
    return os.path.basename(value)


@register.filter()
def FileFind(filepath):
    string = callPathFile(filepath)
    return string


@register.filter()
def FileFindLocation(filepath):
    path = callPathFile(filepath)
    string = f'{settings.BASE_DIR}\\uploads\\resumes\\{path}'
    return string