import datetime
import json
import sys

from django.shortcuts import render
from django.template.defaulttags import now
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from commerce.views import BaseViewSet, MultiSerializerViewSetMixin
from patients.models import Bed, Patient, BedStay, Admission, Schedule
from patients.serializers import BedSerializer, PatientSerializer, \
    AdmissionSerializer, ScheduleSerializer


# Create your views here.
class BedViewSet( BaseViewSet):
    queryset = Bed.objects.all()
    
    def get_serializer_class(self, *args, **kwargs):
        return BedSerializer
    
    @list_route(methods=['get'])
    def getBedMap(self,request, *args, **kwargs):
        beds = Bed.objects.all()
        bedmaps = list ( map(lambda bed: { 'bedName':bed.name , 'patient': bed.patient.displayName  if bed.patient else '' , 'bedId': bed.id } , beds) )
        return Response( bedmaps, status=status.HTTP_200_OK)
    
    @detail_route(methods=['put','post'])
    def admitPatient(self,request, *args, **kwargs):
        bed = self.get_object()
        try:
            
            patientId, note = self.getData(request)
            
            patient = Patient.objects.get(id = patientId)
            
            patient.admit(request, note)
            
            self.movePatientIntoBed(request, bed, patient)
           
            return Response( self.get_serializer(bed).data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response(str(err),status=status.HTTP_400_BAD_REQUEST)

        
   
    def getData(self, request):
        data = json.loads(request.data)
        patientId = data['patient']
        note = data['note']
        return patientId, note

    @detail_route(methods=['put','post'])
    def transferPatient(self,request, *args, **kwargs):
        bed = self.get_object()
        try:
            
            patientId, note = self.getData(request)
            
            patient = Patient.objects.get(id = patientId)
            oldBed = patient.getBed()
            
            patient.transfer(note)

            oldBed.vacate()
            self.markBedStayEnd(patient)
            oldBed.save()
            
            self.movePatientIntoBed(request, bed, patient)
            
            print('transferred patient from {0} to {1} '.format(oldBed.name, bed.name))
            return Response( self.get_serializer(bed).data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response(str(err),status=status.HTTP_400_BAD_REQUEST)
        
    @detail_route(methods=['put'])
    def dischargePatient(self,request, *args, **kwargs):
        bed = self.get_object()
        try:
            
            patientId, note = self.getData(request)
            
            patient = Patient.objects.get(id = patientId)
            assert(patient.getBed() != None)
            bed = patient.getBed()
            
            #TODO move to patient model discharge method
            self.markBedStayEnd(patient)
            patient.discharge(note)
            bed.vacate()
            
            bed.save()
            patient.save()
            
            
            
            assert(bed.patient == None)
            assert(patient.getBed() == None)
            return Response( 'discharged patient  from {0} '.format(bed.name), status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response(str(err),status=status.HTTP_400_BAD_REQUEST)
        
    def createBedStay(self, request, bed, patient):
        bedStay = BedStay.objects.create(bed = bed, owner = request.user,
                                         admission = patient.getCurrentAdmission(),
                                         startDate = datetime.date.today())
        
        
    def markBedStayEnd(self,  patient):
        bedStay = patient.getCurrentAdmission().getCurrentBedStay()
        assert(bedStay.endDate == None)
        bedStay.endDate = datetime.date.today()
        bedStay.save()
        
    def movePatientIntoBed(self, request, bed, patient):
        assert(bed.patient == None)
        bed.occupy(patient)
        assert(bed.patient == patient)
        bed.save()
        patient.save()
        self.createBedStay(request, bed, patient)             
        
class PatientViewSet(MultiSerializerViewSetMixin, BaseViewSet):
    serializer_class = PatientSerializer
    
    
    serializer_classes = {
               'writable': PatientSerializer,
               'complete': PatientSerializer,
            }
    
    
    queryset = Patient.objects.all()
    

    def get_serializer_class(self, *args, **kwargs):
        return PatientSerializer
    
    
class AdmissionViewSet( BaseViewSet):
    queryset = Admission.objects.all()
    
    def get_serializer_class(self, *args, **kwargs):
        return AdmissionSerializer
    
class  ScheduleViewSet( BaseViewSet):
    queryset = Schedule.objects.all()
    permission_classes = (permissions.DjangoModelPermissions, permissions.IsAuthenticatedOrReadOnly)
    
    '''
    def __init__(self):
        pass
        #self.permission_classes = (super().permission_classes, permissions.DjangoModelPermissions)
    '''
    
    def get_serializer_class(self, *args, **kwargs):
        return ScheduleSerializer