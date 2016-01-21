from django.shortcuts import render
from django_fsm import get_available_FIELD_transitions, \
    get_available_user_FIELD_transitions
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import detail_route
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from commerce.models import Employee, Department, Skill, EmployeeSkill
from commerce.permissions import IsOwnerOrReadOnly
from commerce.serializers import EmployeeSerializer, DepartmentSerializer, \
    EmployeeLookupSerializer, FullDepartmentSerializer, \
    DepartmentLookupSerializer, \
    EmployeeWritableSerializer, SkillSerializer, EmployeeSkillSerializer, \
    DepartmentWritableSerializer, FullEmployeeSerializer, SkillLookupSerializer


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 10000


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
    
    

class BaseViewSet( viewsets.ModelViewSet):
    
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        
    def  get_massaged_serializer_class(self, serializer_class, writable_serializer_class):
        if self.request.method in ['PATCH', 'POST', 'PUT'] :
            return writable_serializer_class
        else :
            return serializer_class
        
    @detail_route(methods=['get'])
    def complete(self,request, *args, **kwargs):
        self.method = 'complete'
        return self.retrieve(request, *args, **kwargs)
        
    
    @detail_route(methods=['get'])
    def writable(self,request, *args, **kwargs):
        self.method = 'writable'
        return self.retrieve(request, *args, **kwargs)
        
        
    def getTransitionsForState(self, state):
        obj = self.get_object()
        lst = list(get_available_user_FIELD_transitions(obj, self.request.user, obj._meta.get_field(state)) )
        retlist = []
        for i in lst:
            retlist.append(i.name)
            
        retlist.sort()
    
        return Response(retlist)    

# Create your views here.

    
class MultiSerializerViewSetMixin(object):
    
    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'POST', 'PUT'] :
            return self.get_serializer_class_dict('writable')
        else :
            return self.get_serializer_class_dict(self.action)

    
    def get_serializer_class_dict(self, action):
        try:
            return self.serializer_classes[action]
        except (KeyError, AttributeError):
            return super(MultiSerializerViewSetMixin, self).get_serializer_class()
    

# Create your views here.
class EmployeeViewSet(MultiSerializerViewSetMixin, BaseViewSet):
    queryset = Employee.objects.all()  #.select_related('department', 'owner')
    
    #permission_classes = (permissions.IsAuthenticatedOrReadOnly,IsOwnerOrReadOnly,)
    
    serializer_class = EmployeeSerializer
    
    serializer_classes = {
               'writable': EmployeeWritableSerializer,
               'complete': FullEmployeeSerializer,
            }
    
    @detail_route(methods=['put','get'])
    def join(self,request, *args, **kwargs):
        employee = self.get_object()
        employee.join()
        employee.save()
        return Response({'status': 'state changed'})
    
    @detail_route()
    def getAvailableStateTransitions(self, request, *args, **kwargs):
        return self.getTransitionsForState('state')
        
        
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

class DepartmentViewSet(MultiSerializerViewSetMixin,BaseViewSet):
    queryset = Department.objects.all()
    
    serializer_class = DepartmentSerializer
    
    serializer_classes = {
               'writable': DepartmentWritableSerializer,
               'complete': FullDepartmentSerializer,
            }


class DepartmentCompleteViewSet(DepartmentViewSet):
    serializer_class = FullDepartmentSerializer
    
class DepartmentWritableViewSet(DepartmentViewSet):
    serializer_class = DepartmentWritableSerializer
    
class SkillLookupViewSet(viewsets.ModelViewSet):
    
    pagination_class = LargeResultsSetPagination
    
    queryset = Skill.objects.all()
    serializer_class = SkillLookupSerializer
    
class SkillViewSet( viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    
    def get_serializer_class(self, *args, **kwargs):
        return SkillSerializer