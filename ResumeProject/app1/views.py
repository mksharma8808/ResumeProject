from django.shortcuts import render,redirect,get_object_or_404
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
from .models import Users, Resumes
from django.contrib import messages
from django.conf import settings
from django.views import View
import re
# from django.contrib import messages
# Create your views here.

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'

def check(email):
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False


# def callPathFile(path):
#     filepath = path[1:]
#     string = ''
#     c = 0
#     for i in range(len(filepath)):
#         if filepath[i] in ('%','2','0'):
#             c += 1
#             if(c == 3):
#                 c = 0
#                 string += ' '
#         else:
#             if(c == 3):
#                 c = 0
#                 string += ' '
#             else:
#                 string += filepath[i]
#     return string




def Index(request):
    id = request.session.get('id',False)
    if id:
        return redirect('/profile/')
    return render(request,"login_page.html",{'index':"msg"})

def login(request):
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if not email:
            messages.info(request, "Please enter email!")
            return HttpResponseRedirect('/')
        if not password:
            messages.info(request, "Please enter password!")
            return HttpResponseRedirect('/')
        users = Users.objects.all()
        emailboolean = False
        for user in users:
            if email == user.email:
                emailboolean = True
                if password == user.password:
                    request.session['id'] = user.id
                    return redirect('/profile/')
                    # return JsonResponse({'success':True,'url_pattern':'/profile/','message': 'Login Success'}, status=200)
        if not emailboolean:
            messages.info(request, "Invalid email!")
            # return JsonResponse({'success':False,'message': 'Invalid email!'}, status=200)
        else:
            messages.info(request, "Invalid password!")
            # return JsonResponse({'success': False, 'message': 'Invalid password!'}, status = 200)
        return HttpResponseRedirect('/')
    id = request.session.get('id', False)
    if id:
        return HttpResponseRedirect('/')
    return render(request,"login_page.html",{'index':"msg"})

def register(request):
    if request.method == "POST":
        email = request.POST.get('email')
        if not email:
            messages.warning(request, "Please enter email!")
            return HttpResponseRedirect('/register/')
        booleanValue = check(email)
        if not booleanValue:
            messages.error(request, "Please check your email!")
            return redirect('/register/')
            # return JsonResponse({'success':False,'message': 'Please check your email!!'}, status=200)
        password = request.POST.get('password')
        if not password:
            messages.warning(request, "Please enter password!")
            return redirect('/register/')
        repassword = request.POST.get('repassword')
        if not repassword:
            messages.warning(request, "Please enter re-password!")
            return redirect('/register/')
        if password != repassword:
            messages.warning(request, "Both password doesn't matched!")
            return redirect('/register/')
        try:
            obj = Users.objects.get(email=email)
        except Users.DoesNotExist:
            obj = False
        if obj:
            messages.error(request, 'User Already Registered!')
            return redirect('/register/')
            # return JsonResponse({'success': True,'message': 'User Already Registered!!!','url_pattern':'/register/'}, status=200)
        else:
            set_user = Users(email=email,password=password)
            set_user.save()
            # request.session['id'] = set_user.id
            # print(request.session['id'])
            messages.success(request, 'Registeration successfully!')
            return redirect('/register/')
            # return JsonResponse({'success': True,'message': 'Registeration successfully!!!','url_pattern':'/login/'}, status=200)
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
                if not files:
                    messages.warning(request, "Please fill the files!")
                    return HttpResponseRedirect('/profile/')
                    # return JsonResponse({'success': False, 'message': 'No files uploaded!'}, status=400)
                pdf = request.POST.get("allimages").lower()
                pdf = pdf.split(',')
                indication = True
                wrongfilename = ''
                for file in files:
                    # count += 1
                    if not file.name.lower().endswith(('.pdf', '.doc', '.docx', '.txt')):
                        wrongfilename += f"{file.name},"

                        # return redirect('/profile/')
                        # return JsonResponse({'success': False, 'message': f'Invalid file type: {file.name}'}, status=400)
                    
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
                    elif file.name.lower() in pdf:
                        
                        indication = False
                        Resumes.objects.create(
                            resume=file, 
                            ruid_id=id,
                            created_at_time=datetime.now
                        )
                # print(count)
                if wrongfilename:
                    messages.warning(request,f"Invalid file type: {wrongfilename[:len(wrongfilename)-1]}")
                elif indication:
                    messages.warning(request, "Nothing to update files!")
                else:
                    messages.success(request,f"Files upload successfully!")
                return redirect('/profile/')
            
            except Exception as msg:
                print(msg)
                messages.warning(request, "something error found!!!")
                return HttpResponseRedirect('/profile/')
                # return JsonResponse({'success': False}, status = 404)
        
        return HttpResponseRedirect('/profile/')
    messages.info(request, "Please login!!")
    return redirect('/profile/')
    # return JsonResponse({'success':False,'message':"Please login!!"}, status=200)

# def filterResume(request):
#     id = request.session.get('id',False)
#     if id:
#         # resumes = Resumes.objects.all()
#         # resumes = Resumes.objects.filter(ruid_id=id)
#         # return render(request, "filter.html", {'resumes': resumes})
#         return render(request, "filter.html")
#     return redirect('/')


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


# def searchResume(request):
#     id = request.session.get('id',False)
#     if id:
#         if request.method == 'POST':
#             search = request.POST.get('searchResume').lower()
#             resume = Resumes.objects.filter(ruid_id = id)
#             result = []

#             for data in resume:
#                 searchdata = search.split(' ')
#                 len_of_search = len(searchdata)
#                 # print(searchdata,len_of_search)
#                 checkincr = 0
#                 string = f'{data.resume.url}'
#                 string = pathfile(string)
#                 string = f'{settings.BASE_DIR}{string}'

#                 try:
#                     reader = PdfReader(string)
#                     # print(len(reader.pages))
#                     for i in range(len(reader.pages)):
#                         page = reader.pages[i]
#                         data1 = page.extract_text()                    
#                         data2 = data1.lower()
#                         # print(data2)
#                         for i in range(len_of_search):
#                             for search in searchdata:
#                                 if search in data2:
#                                     # print(searchdata)
#                                     checkincr += 1
#                                     searchdata.remove(search)
#                         # print(checkincr)
#                         if checkincr == len_of_search:
#                             # print("added now")
#                             # checkincr = 0
#                             result.append({'data': data})
#                             break

#                 except Exception as msg:
#                     print(msg)
#                     return JsonResponse({'success': False, 'msg': 'something error found'}, status=200)
#             if result:
#                 print(result)
#                 return render(request,"userprofile.html", {'resumes': result,'filter_id': 'success'})
#             else:
#                 return JsonResponse({'success': True, 'msg': 'not found'}, status=200)
#         resume = Resumes.objects.filter(ruid_id = id)     
#         return render(request,"userprofile.html",{'resumes': resume})
#     return redirect('/login/')

class User_Filter_resumes(View):
    def post(self,request):
        self.id = request.session.get('id',False)
        # if not self.id:
        #     return redirect('/')
        self.search = request.POST.get('searchResume').lower()
        self.resume = Resumes.objects.filter(ruid_id = self.id)
        self.result = []

        for data in self.resume:
            self.searchdata = self.search.split(' ')
            self.len_of_search = len(self.searchdata)
            # print(searchdata,len_of_search)
            self.checkincr = 0
            self.string = f'{data.resume.url}'
            self.string = pathfile(self.string)
            self.string = f'{settings.BASE_DIR}{self.string}'

            try:
                self.reader = PdfReader(self.string)
                # print(len(reader.pages))
                for i in range(len(self.reader.pages)):
                    self.page = self.reader.pages[i]
                    self.data1 = self.page.extract_text()                    
                    self.data2 = self.data1.lower()
                    # print(self.data2)
                    for i in range(self.len_of_search):
                        for search in self.searchdata:
                            if search in self.data2:
                                self.checkincr += 1
                                self.searchdata.remove(search)
                    if self.checkincr == self.len_of_search:
                        self.result.append({'data': data})
                        break

            except Exception as msg:
                print(msg)
                messages.warning(request, "something error found!!!")
                return redirect('/profile/')
                # return render(request,"dashboard.html", {'resumes': self.resume})
                # return JsonResponse({'success': False, 'msg': 'something error found'}, status=200)
        if self.result:
            # print(self.result)
            return render(request,"userprofile.html", {'resumes': self.result,'filter_id': 'success'})
        else:
            messages.warning(request, "Resume not found!!!")
            return redirect('/profile/')
            # return render(request,"dashboard.html", {'resumes': self.resume})
            # return JsonResponse({'success': True, 'msg': 'not found'}, status=200)
    def get(self,request):
        self.id = request.session.get('id',False)
        if not self.id:
            return redirect('/')
        return HttpResponseRedirect('/profile/')


# class Search_Resume(View):
#     def get(self,request):
#         self.id = request.session.get('id',False)
#         if not self.id:
#             return redirect('/')
#         self.resume = Resumes.objects.filter(ruid_id = self.id)
#         return render(request,"userprofile.html",{'resumes': self.resume})


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
    
def multiple_delete_resume(request):
    if request.method == "POST":
        values = request.POST.get('checkbox_selection')
        if not values:
            messages.warning(request, "Please select the files!")
            return redirect('/')
        data = values.split(',')
        for val in data:
            resume = get_object_or_404(Resumes, id=int(val))
            resume.delete()
        messages.success(request,f"Total {len(data)} files deleted!")
    return HttpResponseRedirect('/')

def admin_multiple_delete_resume(request):
    if request.method == "POST":
        values = request.POST.get('checkbox_selection')
        if not values:
            messages.warning(request, "Please select the files!")
            return redirect('/resumes/')
        data = values.split(',')
        for val in data:
            resume = get_object_or_404(Resumes, id=int(val))
            resume.delete()
        messages.success(request,f"Total {len(data)} files deleted!")
    return HttpResponseRedirect('/resumes/')
    
def admin_delete_resume(request, resume_id):
    try:
        resume = get_object_or_404(Resumes, id=resume_id)
        resume.delete()
    except Exception as msg:
        print(msg)
    finally:
        return HttpResponseRedirect('/dashboard/')
    

class Admin_Panel(View):
    def post(self,request):
        self.email = request.POST.get('email')
        self.password = request.POST.get('password')
        if not self.email or not self.password:
            messages.warning(request,"Please Enter email & password")
            return HttpResponseRedirect('/admin/')
        if self.email != 'admin123@gmail.com':
            messages.warning(request, "Incorrect Admin Email!!")
            return HttpResponseRedirect('/admin/')
            # return JsonResponse({'status': False,'message': 'Incorrect Admin Email!!'}, status=200)
        if self.password != 'admin123':
            messages.warning(request, "Incorrect Admin Password!!")
            return HttpResponseRedirect('/admin/')
            # return JsonResponse({'status': False,'message': 'Incorrect Admin Password!!'}, status=200)
        request.session['admin'] = 'admin'
        # messages.success(request,"Successfully Admin login")
        return redirect('/dashboard/')
        # return JsonResponse({'status': True,'message': 'Successfully Admin login','url_pattern': '/dashboard/'}, status=200)
    
    def get(Self,request):
        admin = request.session.get('admin',False)
        if admin:
            return redirect('/dashboard/')
        return render(request,"adminlogin.html")
    
class Admin_Dashboard(View):
    def get(self,request):
        self.admin = request.session.get('admin',False)
        if not self.admin:
            return redirect('/admin/')
        return render(request,"dashboard.html")
    def post(self,request):
        pass
    

class Admin_Logout(View):
    def get(self,request):
        self.admin = request.session.get('admin',False)
        if self.admin:
            del request.session['admin']
        return redirect('/admin/') 

# print("Dict:",list(globals))

class All_users(View):
    def get(self,request):
        self.admin = request.session.get('admin',False)
        if not self.admin:
            return redirect('/admin/')
        self.users_obj = Users.objects.all()
        return render(request, 'dashboard.html', {'users': self.users_obj})
    
class All_resumes(View):
    def get(self,request):
        self.admin = request.session.get('admin',False)
        if not self.admin:
            return redirect('/admin/')
        self.resumes = Resumes.objects.all()[::-1]
        val = self.resumes[0].id
        # print(val)
        return render(request,"dashboard.html",{'resumes': self.resumes,'serial': val})
    
def delete_resumes(id):
    obj = Resumes.objects.filter(ruid_id=id)
    for resume in obj:
        res = get_object_or_404(Resumes, id=resume.id)
        res.delete()

def delete_user(request, user_id):
    try:
        user = Users.objects.get(id = user_id)
        delete_resumes(user.id)
        id = request.session.get('id', False)
        if id:
            if id == user_id:
                del request.session['id']
        user.delete()
    except Exception as msg:
        print(msg)
    finally:
        return HttpResponseRedirect('/users/')
    
class Filter_resumes(View):
    def post(self,request):
        self.search = request.POST.get('searchResume').lower()
        self.resume = Resumes.objects.all()
        self.result = []

        for data in self.resume:
            self.searchdata = self.search.split(' ')
            self.len_of_search = len(self.searchdata)
            # print(searchdata,len_of_search)
            self.checkincr = 0
            self.string = f'{data.resume.url}'
            self.string = pathfile(self.string)
            self.string = f'{settings.BASE_DIR}{self.string}'

            try:
                self.reader = PdfReader(self.string)
                # print(len(reader.pages))
                for i in range(len(self.reader.pages)):
                    self.page = self.reader.pages[i]
                    self.data1 = self.page.extract_text()                    
                    self.data2 = self.data1.lower()
                    # print(self.data2)
                    for i in range(self.len_of_search):
                        for search in self.searchdata:
                            if search in self.data2:
                                self.checkincr += 1
                                self.searchdata.remove(search)
                    if self.checkincr == self.len_of_search:
                        self.result.append({'data': data})
                        break

            except Exception as msg:
                print(msg)
                messages.warning(request, "something error found")
                return redirect('/resumes/')
                # return render(request,"dashboard.html", {'resumes': self.resume})
                # return JsonResponse({'success': False, 'msg': 'something error found'}, status=200)
        if self.result:
            # print(self.result)
            return render(request,"dashboard.html", {'resumes': self.result,'filter_id': 'success'})
        else:
            messages.warning(request, "Resume not found")
            return redirect('/resumes/')
            # return render(request,"dashboard.html", {'resumes': self.resume})
            # return JsonResponse({'success': True, 'msg': 'not found'}, status=200)
    def get(self,request):
        self.admin = request.session.get('admin',False)
        if not self.admin:
            return redirect('/admin/')
        return HttpResponseRedirect('/resumes/')
    
class Filter_delete_resumes(View):
    def get(self,request,resume_id):
        try:
            resume = get_object_or_404(Resumes, id=resume_id)
            resume.delete()
        except Exception as msg:
            print(msg)
        finally:
            return HttpResponseRedirect('/filter-resumes/')
