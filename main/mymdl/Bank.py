

from django.db import models

class CreditCardBase(models.Model): 

           ccNumber = models.CharField(null = False, blank = True  ,  max_length=30)
    
           expiry = models.DateField(null = False, blank = True  , )