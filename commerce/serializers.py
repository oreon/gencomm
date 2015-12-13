
from rest_framework import serializers

from commerce.models import Employee, Department, Skill, EmployeeSkill


class SkillSerializer(serializers.ModelSerializer):
    
    displayName = serializers.ReadOnlyField()

    class Meta:
        model = Skill



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

class EmployeeSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeSkill
        exclude = ('employee',)


class EmployeeWritableSerializer(serializers.ModelSerializer):
    #department = DepartmentLookupSerializer()
    employeeSkills = EmployeeSkillSerializer(many=True)
    class Meta:
        model = Employee
        #depth = 1
        
    def create(self, validated_data):
        employeeSkills = validated_data.pop('employeeSkills')
        employee = Employee.objects.create(**validated_data)
        for oi in employeeSkills:
            EmployeeSkill.objects.create(employee=employee, **oi)
        return employee

    
    def update(self, instance, validated_data):
        EmployeeSkill.objects.filter(employee=instance).delete()
        employeeSkills = validated_data.pop('employeeSkills')
        for item in employeeSkills:
            EmployeeSkill.objects.create(employee=instance, **item)
        return super(EmployeeWritableSerializer, self).update( instance, validated_data)
        
class EmployeeSerializer(  serializers.ModelSerializer,):
    department = DepartmentLookupSerializer()
    employeeSkills = EmployeeSkillSerializer(many=True)
    
    class Meta:
        model = Employee
        #depth = 1
        
    
        
class FullDepartmentSerializer(serializers.ModelSerializer):
    
    employees = EmployeeSerializer(many=True, read_only=True)
    
    class Meta(DepartmentSerializer.Meta):
        model = Department
        
        