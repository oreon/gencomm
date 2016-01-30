import datetime

from auditlog.registry import auditlog
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db import models, transaction
from django.db.models.signals import m2m_changed
from django_fsm import FSMField, transition, ConcurrentTransitionMixin

from commerce.models import Person, Gender, Employee
from commerce.modelsBase import BaseModel, MTManager
import pandas as pd
from patients.helpers import calcDates
from pip.cmdoptions import editable



# Create your models here.
class Patient(ConcurrentTransitionMixin, Person): 

    state = FSMField(default='outpatient', protected=True, editable=False)
    
    schedules = models.ManyToManyField("Schedule",  blank=True,  related_name="schedules")
    
    user = models.OneToOneField(User, related_name = 'patientUser', editable=False, on_delete=models.CASCADE, null = True, blank = True)
    
    objects = MTManager()
    
    class Admin:
        list_display = ('displayName', 'firstName', 'lastName', 'state')
        list_filter = ('dob', 'gender')
        ordering = ('-id',)
        search_fields = ('firstName','lastName', 'dob')
    

    def getBed(self):
        try:
            return self.bed
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
        return   ' '.join([super().__str__() , str(self.age()) , self.gender]);
     
    @transition(field=state, source='outpatient', target='admitted')
    def admit(self, bed, request, note):
        admission = Admission.objects.create( owner = request.user , patient = self, notes = note)
        admission.movePatientIntoBed(bed)
        
    
    @transition(field=state, source='admitted', target='admitted')
    def transfer(self, newbed, note):
        bed = self.getBed()
        self.getCurrentAdmission().markBedStayEnd()
        self.getCurrentAdmission().movePatientIntoBed(newbed)
         
    
    @transition(field=state, source='admitted', target='outpatient')
    def discharge(self, note):
        #self.bed = None
        admission = self.getCurrentAdmission()
        admission.dischargeDate = datetime.date.today()
        #admission.dischargeNote = note
        admission.save()
        pass
    
   


class ProfilePhoto(models.Model):

    profile = models.ForeignKey(Patient, related_name='photos')
    title = models.CharField(max_length=1000, null=True, blank=True)
 #   image = models.ImageField(upload_to='images/%Y/%m/%d', null=True, blank=True)

    def __str__(self):
        return self.title or 'noname'


class Ward(BaseModel): 
    
    name = models.CharField(null = False, blank = True,  max_length=30)
    gender =  models.CharField(max_length = 10, choices=Gender, null = False, blank = True)
    
class Bed(BaseModel): 
    
    state = FSMField(default='free')
    
    ward = models.ForeignKey("Ward", related_name='beds')

    name = models.CharField(null = False, blank = True,  max_length=30)
    
    price = models.DecimalField(max_digits=6, decimal_places=2, null = False, blank = True) 
    #models.IntegerField(null = False, blank = True)
    
    patient = models.OneToOneField(Patient, related_name='bed',null = True, blank = True,)
    
    @transition(field=state, source='free', target='occupied')
    def occupy(self, patient):
        self.patient = patient
        pass 
    
    @transition(field=state, source='occupied', target='free')
    def vacate(self):
        self.patient = None 
    
    def __str__(self):
        return ''.join(self.name)
    
    
class Admission(ConcurrentTransitionMixin, BaseModel):
    
    notes = models.TextField(null = False, blank = True)
    patient = models.ForeignKey(Patient, related_name='admission',null = True, blank = True)
    dischargeDate = models.DateField(null = True, blank = True, )
    
    def getCurrentBedStay(self):
        lst = list( filter(lambda x : x.endDate == None , self.bedstays.all() ) )
        assert len(lst) == 1, "Found multiple CURRENT bedstays"
        return lst[0]
    
    def createBedStay(self,  bed):
        bedStay = BedStay.objects.create(bed = bed, owner = self.owner,
                                         admission = self,
                                         startDate = datetime.date.today())
        
        
    def markBedStayEnd(self):
        bedStay = self.getCurrentBedStay()
        assert(bedStay.endDate == None)
        bedStay.endDate = datetime.date.today()
        bedStay.save()
        
    def movePatientIntoBed(self, bed ):
        #assert(self..patient == None)
        bed.occupy(self.patient)
        assert(bed.patient == self.patient)
        self.createBedStay( bed)
        
        
        
    
    

class BedStay(BaseModel): 
    
    admission = models.ForeignKey(Admission, related_name='bedstays', on_delete=models.CASCADE)

    name = models.CharField(null = False, blank = True,  max_length=30)
    
    startDate = models.DateField(null = False, blank = False, )
    endDate = models.DateField(null = True, blank = True, )
    
    #patient = models.ForeignKey(Patient, related_name='bedstay')
    
    bed = models.ForeignKey(Bed, related_name='bedstay')
    
    def __str__(self):
        return ''.join(self.name)
    

    
class Schedule(BaseModel):
    
    name = models.CharField(null = False, blank = True,  max_length=30)
    
    def __str__(self):
        return ''.join(self.name)
    
    
class ScheduleProcedure(BaseModel): 
    
    schedule = models.ForeignKey(Schedule, related_name='procedures', on_delete=models.CASCADE)
    
    name = models.CharField(null = False, blank = True,  max_length=30)
    
    frequency = models.IntegerField(null = False, blank = True,  )
    
    def __str__(self):
        return ' '.join(self.name)
    
    class Meta:
        unique_together = ("schedule", "name")
    
class PatientScheduleProcedure(BaseModel): 
    
    scheduleProcedure = models.ForeignKey(ScheduleProcedure, related_name='pocedures', on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, related_name='scheduledProcedures', on_delete=models.CASCADE)
    date = models.DateField(null = False, blank = False, )
    notes = models.TextField(null = False, blank = True )
    performDate = models.DateField(null = True, blank = True, )
    
    class Meta:
        unique_together = ("scheduleProcedure", "date", "patient")
    

class Appointment(BaseModel):

    patient = models.ForeignKey(Patient, related_name='appointments',null = False,  )
    
    doctor = models.ForeignKey(Employee, related_name='appointments',null = False, limit_choices_to={'user.groups': True}, )
    
    slot = models.DateTimeField()
    
    class Meta:
        unique_together = (("patient", "slot"), ("doctor", "slot"))
        
        
        
@transaction.atomic
    #@staticmethod       
def ptSchedule_changed(sender, instance,  **kwargs):
        
    patient = instance
    pk_set = kwargs.pop('pk_set', None)
    action = kwargs.pop('action', None)
    
    if action == 'pre_add':
        patient.scheduledProcedures.filter(performDate__isnull = True).delete()
    
    elif action == 'post_add':

        for schedule in patient.schedules.all():
            for procedure in schedule.procedures.all():
                dates = calcDates(procedure.frequency )
                for date in dates:
                    try:
                        PatientScheduleProcedure.objects.create(patient = patient, scheduleProcedure = procedure, date = date)
                    except Exception as err:
                        print (err) 
    
        

m2m_changed.connect(ptSchedule_changed, sender=Patient.schedules.through)



        
auditlog.register(Schedule)
auditlog.register(Ward)

auditlog.register(Patient)
auditlog.register(Bed)
auditlog.register(Appointment)