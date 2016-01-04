
from datetime import timezone
import datetime

from django.db import models
from django_fsm import FSMField, transition

import commerce


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

class BaseModel(models.Model):
    
    owner = models.ForeignKey('auth.User', null = False, blank = True)
    added = models.DateTimeField(auto_now_add=True, null = False, blank = True)
    updated = models.DateTimeField(auto_now=True, null = False, blank = True)
    
    class Meta:
        abstract = True
    #serializer.save(owner=self.request.user)


class Person(BaseModel): 

    gender = models.CharField(max_length=1, choices=Gender, null = False, blank = True)
    dob = models.DateField(null = False, blank = True, )
    
    #address = models.ForeignKey(Address, related_name='person')
     
    class Meta:
        abstract = True

        

class Department(BaseModel): 

    name = models.CharField(null = False, blank = True,  max_length=30)
    
    def __str__(self):
        return ''.join(self.name)
    
    @property
    def displayName(self):
        return self.__str__();


class Employee(Person): 

    department = models.ForeignKey(Department, related_name='employees')
    
    firstName = models.CharField(null = False, blank = True,  max_length=30)
    
    lastName = models.CharField(null = False, blank = True,  max_length=30)
    
    state = FSMField(default='hired')
    
    def __str__(self):
        return ''.join([self.firstName , ', ', self.lastName]);
    
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
    
    @property
    def displayName(self):
        return self.__str__()
    
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
    
 


        

    
 
 
     
     


 

    
  
