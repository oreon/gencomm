
from django.db import models

#from commerce.models import  Department, Employee 


class BaseModel(models.Model):
    
    owner = models.ForeignKey('auth.User', null = False, blank = True)
    added = models.DateTimeField(auto_now_add=True, null = False, blank = True)
    updated = models.DateTimeField(auto_now=True, null = False, blank = True)
    
    class Meta:
        abstract = True


class PersonBase(models.Model): 

	 gender = models.CharField(null=False, blank=True  , max_length=30)
	 dob = models.DateField(null=False, blank=True  ,)
	 # address = models.ForeignKey(Address, related_name='person')
	 class Meta:
	 	abstract = True
	 
        

 
class DepartmentBase(BaseModel): 

     name = models.CharField(null=False, blank=True  , max_length=30)
     class Meta:
        abstract = True

class EmployeeBase(PersonBase): 

	 department = models.ForeignKey(DepartmentBase , unique=True)
	 firstName = models.CharField(null=False, blank=True  , max_length=30)
	 lastName = models.CharField(null=False, blank=True  , max_length=30)
	 class Meta:
	 	abstract = True




  
