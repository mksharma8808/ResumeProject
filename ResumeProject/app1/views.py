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
        data = Resumes.objects.all().values('resume')
        result = {'userlogin': id, 'data': data}
        # return render(request,"userprofile.html",{'data': data})
        return render(request, "userprofile.html", result)
    else:
        return redirect('/')

def logoutpage(request):
    id = request.session.get('id',False)
    if id:
        del request.session['id']
    return redirect('/')

from django.core.files.storage import FileSystemStorage

def updateResume(request):
    id = request.session.get('id',False)
    if id:
        if request.method == "POST":
            try:
                files = request.FILES.getlist('resume') 
                if not files:
                    return JsonResponse({'success': False, 'message': 'No files uploaded!'}, status=400)
                
                for file in files:
                    if not file.name.lower().endswith(('.pdf', '.doc', '.docx', '.txt')):
                        return JsonResponse({'success': False, 'message': f'Invalid file type: {file.name}'}, status=400)
                    
                    fs = FileSystemStorage(location='uploads/resumes/')
                    filename = fs.save(file.name, file)
                    file_url = fs.url(filename)

                    Resumes.objects.create(
                        resume=file_url,
                        ruid_id=id 
                    )
                return redirect('/profile/')
            except Exception as msg:
                # print(msg)
                return JsonResponse({'success': False}, status = 404)
        return render(request,"userprofile.html")
    return JsonResponse({'success':False,'message':"Please login!!"}, status=200)

def filterResume(request):
    data = Resumes.objects.all().values('resume')
    return render(request,"filter.html", {'data': data})