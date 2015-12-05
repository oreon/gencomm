
from django.db import models

import commerce


class Address(models.Model): 

    street = models.CharField(null = False, blank = True,  max_length=30)
    
    city = models.CharField(null = False, blank = True,  max_length=30)
    
    province = models.CharField(null = False, blank = True,  max_length=30)
    
    class Meta:

        abstract = True
    

Gender = (
    ('M', 'Male'),
    ('F', 'Female'),
    ('U', 'Unknown'),
)


class Person(models.Model): 

    gender = models.CharField(max_length=1, choices=Gender, null = False, blank = True)
    dob = models.DateField(null = False, blank = True, )
    
    #address = models.ForeignKey(Address, related_name='person')
     
    class Meta:
        abstract = True



class Department(models.Model): 

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
    
    def __str__(self):
        return ''.join([self.firstName , ', ', self.lastName]);
    
    @property
    def displayName(self):
        return self.__str__()
    
 


        

    
 
 
     
     


 

    
  
