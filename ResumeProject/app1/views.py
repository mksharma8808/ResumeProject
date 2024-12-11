from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import Users, Resumes
from django.contrib import messages
# Create your views here.

def Index(request):
    # if request.method == "POST":
    #     email = request.POST.get("email")
    #     password = request.POST.get("password")
        # print(email,password)
        # return JsonResponse({'success':True},status_code = 200)
        # return HttpResponse("say hii")
        # users = Users.objects.all()
        # # print("users:",users)
        # for user in users:
        #     # print(user)
        #     if email == user.email and password == user.password:
        #         # messages.SUCCESS(request,"Login Successfully")
        #         request.session['id'] = user.id
        #         return JsonResponse({'success':True,'url_pattern':'/profile/','message': 'Login Success'}, status=200)
        #     # else:
        # return JsonResponse({'success': False, 'message': 'Login denied!!!'}, status = 200)
                # messages.WARNING(request,"Login Denied")
    id = request.session.get('id',False)
    if id:
        return redirect('/profile/')
    return render(request,"login_page.html",{'index':"msg"})

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        print(email,password)
        users = Users.objects.all()
        # print("users:",users)
        for user in users:
            print(user)
            if email == user.email and password == user.password:
                # messages.SUCCESS(request,"Login Successfully")
                request.session['id'] = user.id
                return JsonResponse({'success':True,'url_pattern':'/profile/','message': 'Login Success'}, status=200)
            # else:
        return JsonResponse({'success': False, 'message': 'Login denied!!!'}, status = 200)

    return render(request,"login_page.html",{'index':"msg"})

def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)
        try:
            obj = Users.objects.get(email=email)
        except Users.DoesNotExist:
            obj = False
        if obj:
            return JsonResponse({'success': True,'message': 'User Already Registered!!!','url_pattern':'/login/'}, status=200)
        else:
            set_user = Users(email=email,password=password)
            set_user.save()
            request.session['id'] = set_user.id
            # print(request.session['id'])
            return JsonResponse({'success': True,'message': 'Registeration successfully!!!','url_pattern':'/profile/'}, status=200)
        # return HttpResponse("registeration successfully")
    return render(request,"registeration.html")

def profile(request):
    id = request.session.get('id')
    if id:
        data = {'userlogin': id}
        return render(request, "userprofile.html", data)
    else:
        return redirect('/')

def logoutpage(request):
    id = request.session.get('id',False)
    if id:
        del request.session['id']
    return redirect('/')


def updateResume(request):
    id = request.session.get('id',False)
    print(request)
    if id:
        if request.method == "POST":
            try:
                # print(request)
                # obj = Users.objects.get(id = id)
                data = request.Files['resume']
                # for i in data:
                #     print(i)
                print("data:",data)
                return HttpResponse("submition successfully")
                # print(data)
                # actualData = data.split(',')
                # for i in actualData:
                #     saveobj = Resumes(resume = i, ruid = obj)
                #     saveobj.save()
                # return JsonResponse({'success': True}, status = 200)
            except Exception as msg:
                print(msg)
                return JsonResponse({'success': False}, status = 404)
    return JsonResponse({'success':False,'message':"Please login!!"}, status=200)

def filterResume(request):
    data = Resumes.objects.all()
    return render(request,"filter.html", {'data': data})