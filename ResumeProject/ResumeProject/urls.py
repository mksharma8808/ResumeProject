"""
URL configuration for ResumeProject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app1 import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('admin/', admin.site.urls),
    path('admin/', views.Admin_Panel.as_view()),
    path('dashboard/', views.Admin_Dashboard.as_view()),
    path('admin-logout/', views.Admin_Logout.as_view()),
    path('users/', views.All_users.as_view(), name='users'),
    path('resumes/', views.All_resumes.as_view(), name='resumes'),
    path('filter-resumes/', views.Filter_resumes.as_view(), name='filter_resumes'),
    path('filter-delete-resumes/<int:resume_id>/', views.Filter_delete_resumes.as_view(), name='filter_delete_resumes'),
    path('adminmultiDelete/', views.admin_multiple_delete_resume, name='multi_delete_resume'),
    path('delete-user/<int:user_id>/', views.delete_user),
    path('', views.Index),
    path('register/', views.register),
    path('profile/', views.userProfile),
    path('logout/', views.logoutpage),
    path('login/', views.login),
    path('update/', views.updateResume),
    path('filter/', views.User_Filter_resumes.as_view()),
    # path('search-resume/', views.Search_Resume.as_view(), name= 'search_resume'),
    path('delete-resume/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    path('multiDelete/', views.multiple_delete_resume, name='multi_delete_resume'),
    # path('delete-resume/<int:resume_id>/', views.delete_resume, name='delete_resume'),
    path('admin-delete-resume/<int:resume_id>/', views.admin_delete_resume, name='admin_delete_resume'),
]+static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
