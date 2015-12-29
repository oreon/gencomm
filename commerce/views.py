from django.shortcuts import render
from rest_framework import viewsets

from commerce.models import Employee, Department, Skill, EmployeeSkill
from commerce.serializers import EmployeeSerializer, DepartmentSerializer, \
    EmployeeLookupSerializer, FullDepartmentSerializer, \
    DepartmentLookupSerializer, \
    EmployeeWritableSerializer, SkillSerializer, EmployeeSkillSerializer,\
    DepartmentWritableSerializer


class ReadNestedWriteFlatMixin(object):
    """
    Mixin that sets the depth of the serializer to 0 (flat) for writing operations.
    For all other operations it keeps the depth specified in the serializer_class
    """
    def get_serializer_class(self, *args, **kwargs):
        serializer_class = super(ReadNestedWriteFlatMixin, self).get_serializer_class(*args, **kwargs)
        if self.request.method in ['PATCH', 'POST', 'PUT']:
            serializer_class.Meta.depth = 0
        return serializer_class
    
    
def  get_massaged_serializer_class(serializer_class, request):
        if request.method in ['PATCH', 'POST', 'PUT'] :
            serializer_class.Meta.depth = 0
        else :
            serializer_class.Meta.depth = 1
        return serializer_class


# Create your views here.
class SkillViewSet( viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    
    def get_serializer_class(self, *args, **kwargs):
        return SkillSerializer

# Create your views here.
class EmployeeViewSet( viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    
    def get_serializer_class(self, *args, **kwargs):
        return EmployeeSerializer
        #return get_massaged_serializer_class(EmployeeSerializer, self.request)
        
class EmployeeWritableViewSet(EmployeeViewSet):
    serializer_class = EmployeeWritableSerializer 
    
class EmployeeCompleteViewSet(EmployeeViewSet):
    serializer_class = EmployeeSerializer  
   
class EmployeeLookupViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = EmployeeLookupSerializer


    
class EmployeeSkillViewSet(viewsets.ModelViewSet):
    queryset = EmployeeSkill.objects.all()
    serializer_class = EmployeeSkillSerializer

'''    
class EmployeeCompleteViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all()
    serializer_class = FullEmployeeSerializer
 '''
    
class DepartmentLookupViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentLookupSerializer

class DepartmentViewSet(viewsets.ModelViewSet):
    queryset = Department.objects.all()
    serializer_class = DepartmentSerializer

class DepartmentCompleteViewSet(DepartmentViewSet):
    serializer_class = FullDepartmentSerializer
    
class DepartmentWritableViewSet(DepartmentViewSet):
    serializer_class = DepartmentWritableSerializer
    