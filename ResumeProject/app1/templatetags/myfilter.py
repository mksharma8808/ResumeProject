from django import template
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