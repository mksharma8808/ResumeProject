from django import template
from app1.models import Users

register = template.Library()

@register.filter()
def useremail(id):
    try:
        user = Users.objects.get(id = id)
        return user.email
    except:
        return 'everyone'