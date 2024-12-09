from django.shortcuts import render
from django.http import JsonResponse,HttpResponse
from .models import Users
from django.contrib import messages
# Create your views here.

def Index(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email,password)
        # return JsonResponse({'success':True},status_code = 200)
        # return HttpResponse("say hii")
        users = Users.objects.all()
        for user in users:
            if email == user.email and password == user.password:
                messages.SUCCESS(request,"Login Successfully")
                return render(request,"userprofile.html")
            else:
                messages.WARNING(request,"Login Denied")
    return render(request,"login_page.html",{'index':"msg"})

def register(request):
    return render(request,"registeration.html")

def profile(request):
    return render(request,"userprofile.html")