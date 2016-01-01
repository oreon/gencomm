
from rest_framework import serializers

from commerce.models import Employee, Department, Skill, EmployeeSkill



class EmployeeLookupSerializer(serializers.ModelSerializer):
    
    displayName = serializers.ReadOnlyField()

    class Meta:
        model = Employee
        fields = ('displayName', 'id', )

class DepartmentLookupSerializer(serializers.ModelSerializer):
    
    displayName = serializers.ReadOnlyField()

    class Meta:
        model = Department
        fields = ('displayName', 'id', )




class SkillLookupSerializer(serializers.ModelSerializer):
    
    displayName = serializers.ReadOnlyField()

    class Meta:
        model = Skill
        fields = ('displayName', 'id', )

class EmployeeSkillLookupSerializer(serializers.ModelSerializer):
    
    displayName = serializers.ReadOnlyField()

    class Meta:
        model = EmployeeSkill
        fields = ('displayName', 'id', )
        
        
class DepartmentSerializer(serializers.ModelSerializer):


    displayName = serializers.ReadOnlyField()
    

    class Meta:
        model = Department
        
        

        

class DepartmentWritableSerializer(serializers.ModelSerializer):
    
    displayName = serializers.ReadOnlyField()
    

    class Meta:
        model = Department

class SkillSerializer(serializers.ModelSerializer):
    
    displayName = serializers.ReadOnlyField()

    class Meta:
        model = Skill


class EmployeeSkillWritableSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeSkill
        exclude = ('employee',)
        
class EmployeeSkillSerializer(serializers.ModelSerializer):

    class Meta:
        model = EmployeeSkill
        exclude = ('employee',)
        depth = 1


class EmployeeWritableSerializer(serializers.ModelSerializer):
    #department = DepartmentLookupSerializer()
    employeeSkills = EmployeeSkillWritableSerializer(many=True)
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
        
class EmployeeSerializerOrg(  serializers.ModelSerializer,):
    department = DepartmentLookupSerializer()
    employeeSkills = EmployeeSkillSerializer(many=True)
    
    class Meta:
        model = Employee
        #depth = 1
        
class EmployeeSerializer(serializers.ModelSerializer):

 
    department = DepartmentSerializer()
 

    displayName = serializers.ReadOnlyField()
    
 
    employeeSkills = EmployeeSkillSerializer(many=True)
    
    #def terminate(self):
        
 
    
    class Meta:
        model = Employee
        
        
class FullEmployeeSerializer(EmployeeSerializer):

    class Meta(EmployeeSerializer.Meta):
        model = Employee
        
class FullDepartmentSerializer(DepartmentSerializer):

 
    employees = EmployeeSerializer(many=True, read_only=True)
 
    
    class Meta(DepartmentSerializer.Meta):
        model = Department    

        


        
        
        