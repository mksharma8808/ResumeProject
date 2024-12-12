from django.shortcuts import render,redirect
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
        # count = 0
        # resume = Resumes.objects.all().values('resume')
        # actualpdf = {}
        # for data in resume:
        #     pathfile = callPathFile(data['resume'])
        #     actualpdf.update({f'resume{count}': pathfile})
        #     count += 1
            # # print(pathfile)
            # string = f'{settings.BASE_DIR}'
            # string += f'\\uploads\\resumes\\{pathfile}'


        result = {'userlogin': id}
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
                    # print(file)
                    # try:
                    #     userobj = Users.objects.get(id = int(id))
                    #     data = Resumes(resume = file, ruid_id = userobj)
                    #     data.save()
                    #     print("success")
                    # except Exception as msg:
                    #     print(msg)
                return redirect('/profile/')
            except Exception as msg:
                print(msg)
                return JsonResponse({'success': False}, status = 404)
        return render(request,"userprofile.html")
    return JsonResponse({'success':False,'message':"Please login!!"}, status=200)

def filterResume(request):
    id = request.session.get('id',False)
    if id:
        # data = Resumes.objects.all().values('resume')
        return render(request,"filter.html")
    return redirect('/')



# Create your tests here.
from pypdf import PdfReader


def searchResume(request):
    id = request.session.get('id',False)
    if id:
        if request.method == 'POST':
            search = request.POST.get('searchResume').lower()
            # print(search)
            searchdata = search.split(' ')
            searchincr = len(searchdata)
            # print(searchdata,searchincr)
            resume = Resumes.objects.all().values('resume')
            # print(resume)
            result = {}
            incr = 0

            for data in resume:

                checkincr = 0
                pathfile = callPathFile(data['resume'])
                string = f'{settings.BASE_DIR}'
                string += f'\\uploads\\resumes\\{pathfile}'

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
                            # print("Enterv in success")
                            result.update({f'result{incr}': data['resume']})
                            incr += 1
                            # print(result)
                            break

                except Exception as msg:
                    print(msg)
                    return JsonResponse({'success': False, 'msg': 'something error found'}, status=200)
            if result:
                return render(request,"filter.html", {'data': result.items()})
            else:
                return JsonResponse({'success': True, 'msg': 'not found'}, status=200)
               
        return render(request,"filter.html")
    return redirect('/login/')


