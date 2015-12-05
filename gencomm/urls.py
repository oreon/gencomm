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
from rest_framework import routers

from commerce.views import DepartmentLookupViewSet, DepartmentWritableViewSet, \
    EmployeeCompleteViewSet
from commerce.views import EmployeeViewSet, DepartmentViewSet, \
    EmployeeLookupViewSet, DepartmentCompleteViewSet, EmployeeWritableViewSet


router = routers.SimpleRouter(trailing_slash=False)

router.register(r'employees', EmployeeViewSet)
router.register(r'employeesWritable', EmployeeWritableViewSet)
router.register(r'employeesComplete', EmployeeCompleteViewSet)
router.register(r'employeesLookup', EmployeeLookupViewSet)

router.register(r'departmentsLookup', DepartmentLookupViewSet)
router.register(r'departments', DepartmentViewSet)
router.register(r'departmentsComplete', DepartmentCompleteViewSet)
router.register(r'departmentsWritable', DepartmentWritableViewSet)


urlpatterns = [
    url(r'^api/v1/', include(router.urls)),
    url(r'^admin/', include(admin.site.urls)),
]
