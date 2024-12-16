from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from .models import Users, Resumes
from django.contrib import messages
from django.conf import settings
# Create your views here.


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




def Index(request):
    id = request.session.get('id',False)
    if id:
        return redirect('/profile/')
    return render(request,"login_page.html",{'index':"msg"})

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        # print(email,password)
        users = Users.objects.all()
        # print("users:",users)
        for user in users:
            # print(user)
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
        # print(email,password)
        try:
            obj = Users.objects.get(email=email)
        except Users.DoesNotExist:
            obj = False
        if obj:
            return JsonResponse({'success': True,'message': 'User Already Registered!!!','url_pattern':'/login/'}, status=200)
        else:
            set_user = Users(email=email,password=password)
            set_user.save()
            # request.session['id'] = set_user.id
            # print(request.session['id'])
            return JsonResponse({'success': True,'message': 'Registeration successfully!!!','url_pattern':'/login/'}, status=200)
        # return HttpResponse("registeration successfully")
    return render(request,"registeration.html")

def userProfile(request):
    id = request.session.get('id', False)
    if id:
        resumes = Resumes.objects.filter(ruid_id=id)[::-1]
        return render(request, "userprofile.html", {'resumes': resumes})
    return redirect('/login/')


def logoutpage(request):
    id = request.session.get('id',False)
    if id:
        del request.session['id']
    return redirect('/')

# from django.core.files.storage import FileSystemStorage
# import json
from datetime import datetime

def updateResume(request):
    id = request.session.get('id',False)
    if id:
        if request.method == "POST":
            try:
                files = request.FILES.getlist('resume') 
                # data = json.loads(request.body)
                # print(data)


                if not files:
                    return JsonResponse({'success': False, 'message': 'No files uploaded!'}, status=400)
                
                # count = 0
                for file in files:
                    # count += 1
                    if not file.name.lower().endswith(('.pdf', '.doc', '.docx', '.txt')):
                        return JsonResponse({'success': False, 'message': f'Invalid file type: {file.name}'}, status=400)
                    
                    # fs = FileSystemStorage(location='uploads/resumes/')
                    # filename = fs.save(file.name, file)
                    # file_url = fs.url(filename)

                    # Resumes.objects.create(
                    #     resume=file_url,
                    #     ruid_id=id 
                    # )
                    # print(file)
                    # try:
                    #     userobj = Users.objects.get(id = int(id))
                    #     data = Resumes(resume = file, ruid_id = userobj)
                    #     data.save()
                    #     print("success")
                    # except Exception as msg:
                    #     print(msg)

                    Resumes.objects.create(
                        resume=file, 
                        ruid_id=id,
                        created_at_time=datetime.now
                    )
                # print(count)
                return redirect('/profile/')
            
            except Exception as msg:
                print(msg)
                return JsonResponse({'success': False}, status = 404)
            
        return render(request,"userprofile.html")
    return JsonResponse({'success':False,'message':"Please login!!"}, status=200)

def filterResume(request):
    id = request.session.get('id',False)
    if id:
        # resumes = Resumes.objects.all()
        # resumes = Resumes.objects.filter(ruid_id=id)
        # return render(request, "filter.html", {'resumes': resumes})
        return render(request, "filter.html")
    return redirect('/')


def pathfile(path):
    str1 = ''
    for i in path:
        if i == '/':
            str1 += '\\'
        else:
            str1 += i
    return str1

# Create your tests here.
from pypdf import PdfReader


def searchResume(request):
    id = request.session.get('id',False)
    if id:
        if request.method == 'POST':
            search = request.POST.get('searchResume').lower()
            searchdata = search.split(' ')
            searchincr = len(searchdata)
            resume = Resumes.objects.all()
            result = []

            for data in resume:
                checkincr = 0
                string = f'{data.resume.url}'
                string = pathfile(string)
                string = f'{settings.BASE_DIR}{string}'

                try:
                    reader = PdfReader(string)
                    for i in range(len(reader.pages)):
                        page = reader.pages[i]
                        data1 = page.extract_text()                    
                        data2 = data1.lower()
                        # print(data2)
                        for search in searchdata:
                            if search in data2:
                                checkincr += 1

                        if checkincr == searchincr:
                            result.append({'data': data})
                            break

                except Exception as msg:
                    print(msg)
                    return JsonResponse({'success': False, 'msg': 'something error found'}, status=200)
            if result:
                # print(result)
                return render(request,"filter.html", {'resumes': result})
            else:
                return JsonResponse({'success': True, 'msg': 'not found'}, status=200)
               
        return render(request,"filter.html")
    return redirect('/login/')


# from app1.models import Resumes  # Replace 'yourapp' with the name of your app
# resumes = Resumes.objects.all()
# for resume in resumes:
#     print(resume.resume.url)  # This will print the URL of each uploaded resume


def delete_resume(request, resume_id):
    try:
        resume = get_object_or_404(Resumes, id=resume_id)
        resume.delete()
    except Exception as msg:
        print(msg)
    finally:
        return HttpResponseRedirect('/profile/')