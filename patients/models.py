from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django_fsm import FSMField, transition

from commerce.models import Person
from commerce.modelsBase import BaseModel


# Create your models here.
class Patient(Person): 

    state = FSMField(default='outpatient')
    
    def getBed(self):
        try:
            bedobj = Bed.objects.get(patient = self)
            return bedobj
        except ObjectDoesNotExist :
            return None
        
    def getCurrentAdmission(self):
        try:
            return Admission.objects.get(patient = self ,  dischargeDate = None)
            #admissions = Admission.objects.filter(patient = self ,  dischargeDate = None)
            #return admissions[0]
        except ObjectDoesNotExist :
            return None
      
    
    #bed = models.ForeignKey('bed',null = True, blank = True)
    
    def __str__(self):
        return   ' '.join([super().__str__() , '30' , self.gender]);
     
    @transition(field=state, source='outpatient', target='admitted')
    def admit(self, request):
        admission = Admission.objects.create( owner = request.user , patient = self)
    
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
    patient = models.ForeignKey(Patient, related_name='admission',null = True, blank = True)
    dischargeDate = models.DateField(null = True, blank = True, )
    
    def getCurrentBedStay(self):
        lst = list( filter(lambda x : x.endDate == None , self.bedstays.all() ) )
        assert (len(lst) == 1, "Found multiple CURRENT bedstays")
        return lst[0]
    
    

class BedStay(BaseModel): 
    
    admission = models.ForeignKey(Admission, related_name='bedstays', on_delete=models.CASCADE)

    name = models.CharField(null = False, blank = True,  max_length=30)
    
    startDate = models.DateField(null = False, blank = False, )
    endDate = models.DateField(null = True, blank = True, )
    
    #patient = models.ForeignKey(Patient, related_name='bedstay')
    
    bed = models.ForeignKey(Bed, related_name='bedstay')
    
    def __str__(self):
        return ''.join(self.name)
    

    
    