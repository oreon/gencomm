
from rest_framework import serializers

from commerce.models import Employee, Department



class DepartmentSerializer(serializers.ModelSerializer):
    
    displayName = serializers.ReadOnlyField()

    class Meta:
        model = Department
        
class DepartmentLookupSerializer(serializers.ModelSerializer):
    
    displayName = serializers.ReadOnlyField()

    class Meta:
        model = Department
        fields = ('displayName', 'id', )  
        

class EmployeeLookupSerializer(serializers.ModelSerializer):
    
    displayName = serializers.ReadOnlyField()
    
    class Meta:
        model = Employee
        fields = ('displayName', 'id', )     


class EmployeeWritableSerializer(  serializers.ModelSerializer,):
    #department = DepartmentLookupSerializer()
    class Meta:
        model = Employee
        #depth = 1
        
class EmployeeSerializer(  serializers.ModelSerializer,):
    department = DepartmentLookupSerializer()
    class Meta:
        model = Employee
        #depth = 1
        
        
class FullDepartmentSerializer(serializers.ModelSerializer):
    
    employees = EmployeeSerializer(many=True, read_only=True)
    
    class Meta(DepartmentSerializer.Meta):
        model = Department
        
        