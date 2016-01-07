
from datetime import timezone
import datetime

from django.db import models
from django_fsm import FSMField, transition

import commerce
from commerce.modelsBase import BaseModel
from commerce.modelsBase import DepartmentBase


class Address(models.Model): 

    street = models.CharField(null = False, blank = True,  max_length=30)
    
    city = models.CharField(null = False, blank = True,  max_length=30)
    
    province = models.CharField(null = False, blank = True,  max_length=30)
    
    class Meta:

        abstract = True
    

Gender = (
    ('MALE', 'Male'),
    ('FEMALE', 'Female'),
    ('U', 'Unknown'),
)




class Person(BaseModel): 

    gender = models.CharField(max_length=1, choices=Gender, null = False, blank = True)
    dob = models.DateField(null = False, blank = True, )
    
    firstName = models.CharField(null = False, blank = True,  max_length=30)
    lastName = models.CharField(null = False, blank = True,  max_length=30)
    
    #address = models.ForeignKey(Address, related_name='person')
    @property   
    def displayName(self):
        return self.__str__()
    
    def __str__(self):
        return ''.join([self.firstName , ', ', self.lastName]);
     
    class Meta:
        abstract = True

        

class Department(DepartmentBase): 

    #name = models.CharField(null = False, blank = True,  max_length=30)
    
    def __str__(self):
        return ''.join(self.name)
    
    @property
    def displayName(self):
        return self.__str__();


class Employee(Person): 

    department = models.ForeignKey(Department, related_name='employees')
    
    state = FSMField(default='hired')
    
    
    @transition(field=state, source='hired', target='active')
    def join(self):
        pass
    
    @transition(field=state, source='active', target='suspended')
    def suspend(self):
        pass
    
    @transition(field=state, source='active', target='left')
    def leave(self):
        pass
    
    @transition(field=state, source='[active, suspended]', target='terminated')
    def terminate(self):
        pass
    
    @transition(field=state, source='suspended', target='active')
    def reinstate(self):
        pass
    
    
    
class Skill(models.Model):
    name = models.CharField(null = False, blank = True,  max_length=30)
    
    def __str__(self):
        return self.name
    
    @property
    def displayName(self):
        return self.__str__()
    
class EmployeeSkill(models.Model):
    employee = models.ForeignKey(Employee, related_name='employeeSkills')
    skill = models.ForeignKey(Skill)
    experience   = models.IntegerField(default = 1)
    
 


        

    
 
 
     
     


 

    
  
