
from datetime import timezone
import datetime

from django.contrib.auth.models import User
from django.db import models
from django.db.models.deletion import CASCADE
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

    gender = models.CharField(max_length=6, choices=Gender, null = False, blank = True)
    dob = models.DateField(null = False, blank = True, )
    
    firstName = models.CharField(null = False, blank = True,  max_length=30)
    lastName = models.CharField(null = False, blank = True,  max_length=30)
    
    def age(self):
        return int((datetime.date.today() - self.dob).days / 365.25  )
    
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
    
    user = models.OneToOneField(User, related_name = 'employeeUser', on_delete=models.CASCADE, null = True, blank = True)
    
    
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
    
class Asset(models.Model): 
    name = models.CharField(null = False, blank = True,  max_length=30)
    department = models.ForeignKey(Department, related_name='assets') 
    price = models.IntegerField(default = 100)
    
class Skill(models.Model):
    name = models.CharField(null = False, blank = True,  max_length=30)
    
    def __str__(self):
        return self.name
    
    @property
    def displayName(self):
        return self.__str__()
    
class EmployeeSkill(models.Model):
    employee = models.ForeignKey(Employee, related_name='employeeSkills', on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill)
    experience   = models.IntegerField(default = 1)
    
    class Meta:
        order_with_respect_to = 'employee'
        unique_together = ("employee", "skill")
    
 


        

    
 
 
     
     


 

    
  
