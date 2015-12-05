
from django.db import models

#from commerce.models import  Department, Employee 


class PersonBase(models.Model): 

	 gender = models.CharField(null=False, blank=True  , max_length=30)
	 dob = models.DateField(null=False, blank=True  ,)
	 # address = models.ForeignKey(Address, related_name='person')
	 class Meta:
	 	abstract = True
	 
        

 
class DepartmentBase(models.Model): 

     name = models.CharField(null=False, blank=True  , max_length=30)
     class Meta:
        abstract = True

class EmployeeBase(PersonBase): 

	 department = models.ForeignKey(DepartmentBase , unique=True)
	 firstName = models.CharField(null=False, blank=True  , max_length=30)
	 lastName = models.CharField(null=False, blank=True  , max_length=30)
	 class Meta:
	 	abstract = True




  
