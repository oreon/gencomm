from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from gencomm import settings
from patients.models import Patient


from django.db import models
from django.contrib.auth.models import AbstractUser
 
'''
class CustomUser(AbstractUser):
    pass
 
class PatientUser(CustomUser):
    pass
 
class EmployeeUser(CustomUser):
    spcialization = models.CharField(null=True , blank= True)

'''


# Create your models here.
@receiver(post_save, sender= User)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    # TODO - use this signal to create blank patient profile 
    if created:
        owner1 = User.objects.get(id = 1)
        profile = Patient(user=instance)
        profile.save()

    pass