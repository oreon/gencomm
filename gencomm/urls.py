"""gencomm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic.base import TemplateView
from rest_framework import routers

from basicauth.views import UserViewSet
from commerce.views import DepartmentLookupViewSet, DepartmentWritableViewSet, \
    EmployeeCompleteViewSet, SkillViewSet, EmployeeSkillViewSet, \
    SkillLookupViewSet
from commerce.views import EmployeeViewSet, DepartmentViewSet, \
    EmployeeLookupViewSet, DepartmentCompleteViewSet, EmployeeWritableViewSet
#import gencomm.views
from patients.views import PatientViewSet, BedViewSet, AdmissionViewSet, \
    ScheduleViewSet, patient_view


router = routers.SimpleRouter(trailing_slash=False)

router.register(r'skills', SkillViewSet)
router.register(r'skillsLookup', SkillLookupViewSet)


router.register(r'employees', EmployeeViewSet)
router.register(r'employeesWritable', EmployeeWritableViewSet)
router.register(r'employeesComplete', EmployeeCompleteViewSet)
router.register(r'employeesLookup', EmployeeLookupViewSet)
router.register(r'employeeSkills', EmployeeSkillViewSet)


router.register(r'departmentsLookup', DepartmentLookupViewSet)
router.register(r'departments', DepartmentViewSet, base_name='departments')
router.register(r'departmentsComplete', DepartmentCompleteViewSet)
router.register(r'departmentsWritable', DepartmentWritableViewSet)

router.register(r'appusers', UserViewSet)

router.register(r'patients', PatientViewSet)
router.register(r'beds', BedViewSet)
router.register(r'admissions', AdmissionViewSet)
router.register(r'schedules', ScheduleViewSet)





urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
 #   url(r'^$', gencomm.views.home, name='home'),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls')),
    url(r'^api-token-auth/', 'rest_framework_jwt.views.obtain_jwt_token'),
    url(r'^accounts/', include('allauth.urls')),
  #  url(r'^comm/', include('commerce.urls')),
    #url(r'^grappelli/', include('grappelli.urls')),
   # url(r'^admin_tools/', include('admin_tools.urls')),
    
    url(r'^admin/patients/patient/viewPatient/(\d+)/$', patient_view), 
    url(r'^admin/', include(admin.site.urls)),
    
    
    url(r'^signup/$', TemplateView.as_view(template_name="signup.html"),
        name='signup'),
    url(r'^email-verification/$',
        TemplateView.as_view(template_name="email_verification.html"),  
        name='email-verification'),
    url(r'^login/$', TemplateView.as_view(template_name="login.html"),
        name='login'),
    url(r'^password-reset/$',
        TemplateView.as_view(template_name="password_reset.html"),
        name='password-reset'),
    url(r'^password-reset/confirm/$',
        TemplateView.as_view(template_name="password_reset_confirm.html"),
        name='password-reset-confirm'),

    url(r'^user-details/$',
        TemplateView.as_view(template_name="user_details.html"),
        name='user-details'),
    url(r'^password-change/$',
        TemplateView.as_view(template_name="password_change.html"),
        name='password-change'),
]
