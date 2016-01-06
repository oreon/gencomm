from django.db import models
from django_fsm import FSMField, transition

from commerce.models import Person
from commerce.modelsBase import BaseModel


# Create your models here.
class Patient(Person): 

    state = FSMField(default='outpatient')
     
    @transition(field=state, source='outpatient', target='admitted')
    def admit(self):
        pass 
    
    @transition(field=state, source='admitted', target='admitted')
    def transfer(self):
        pass 
    
    @transition(field=state, source='admitted', target='outpatient')
    def discharge(self):
        pass 
    

        

class Bed(BaseModel): 
    
    state = FSMField(default='free')

    name = models.CharField(null = False, blank = True,  max_length=30)
    
    price = models.IntegerField(null = False, blank = True)
    
    patient = models.ForeignKey(Patient, related_name='bed',null = True, blank = True)
    
    @transition(field=state, source='free', target='occupied')
    def occupy(self, patient):
        self.patient = patient
        pass 
    
    @transition(field=state, source='occupied', target='free')
    def vacate(self):
        self.patient = None 
    
    def __str__(self):
        return ''.join(self.name)
    
    
class Admission(BaseModel):
    
    notes = models.TextField(null = False, blank = True)
    

class BedStay(BaseModel): 
    
    admission = models.ForeignKey(Admission, related_name='bedstays')

    name = models.CharField(null = False, blank = True,  max_length=30)
    
    startDate = models.DateField(null = False, blank = False, )
    endDate = models.DateField(null = True, blank = True, )
    
    patient = models.ForeignKey(Patient, related_name='bedstay')
    
    bed = models.ForeignKey(Bed, related_name='bedstay')
    
    def __str__(self):
        return ''.join(self.name)
    

    
    