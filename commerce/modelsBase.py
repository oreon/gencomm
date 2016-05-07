
import inspect

from auditlog.models import AuditlogHistoryField
from django.contrib.auth.models import User
from django.db import models


def get_request():
    """Walk up the stack, return the nearest first argument named "request"."""
    frame = None
    try:
        for f in inspect.stack()[1:]:
            frame = f[0]
            code = frame.f_code
            if code.co_varnames and code.co_varnames[0] == "request":
                return frame.f_locals['request']
    finally:
        del frame


#from commerce.models import  Department, Employee 
class MTManager(models.Manager):
    def get_query_set(self):
        return super(MTManager, self).get_query_set().filter(owner=get_request().user)


class BaseModel(models.Model):
    
    owner = models.ForeignKey(User, null = True, blank = True, editable=False)
    added = models.DateTimeField(auto_now_add=True, null = False, blank = True)
    updated = models.DateTimeField(auto_now=True, null = False, blank = True)
    history = AuditlogHistoryField()
    
    objects = MTManager()
    
    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        if 'form' in kwargs:
            form=kwargs['form']
        else: 
            form=None

        #if self.pk is None and get_request() is not None:
        #   self.owner=get_request().user
        super().save(*args, **kwargs)

class PersonBase(models.Model): 

	gender = models.CharField(null=True, blank=False  , max_length=30)
	dob = models.DateField(null=True, blank=False  ,)
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




  
