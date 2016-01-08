import datetime
import json
import sys

from django.shortcuts import render
from django.template.defaulttags import now
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from commerce.views import BaseViewSet
from patients.models import Bed, Patient, BedStay, Admission
from patients.serializers import BedSerializer, PatientSerializer, \
    AdmissionSerializer


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
            
            patient.transfer()

            oldBed.vacate()
            self.markBedStayEnd(patient)
            
            self.movePatientIntoBed(request, bed, patient)
            
            oldBed.save()
            
            print('transferred patient to {0} from {1} '.format(bed.name, oldBed.name))
            return Response( self.get_serializer(bed).data, status=status.HTTP_200_OK)
        except Exception as err:
            return Response(str(err),status=status.HTTP_400_BAD_REQUEST)
        
    @detail_route(methods=['put'])
    def dischargePatient(self,request, *args, **kwargs):
        bed = self.get_object()
        try:
            
            patientId, note = self.getData(request)
            
            patient = Patient.objects.get(id = patientId)
            bed = patient.getBed()
            
            patient.discharge()
            bed.vacate()
            
            bed.save()
            patient.save()
            
            self.markBedStayEnd(patient)
            
            assert(bed.patient == None)
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
        
class PatientViewSet( BaseViewSet):
    queryset = Patient.objects.all()
    

    def get_serializer_class(self, *args, **kwargs):
        return PatientSerializer
    
    
class AdmissionViewSet( BaseViewSet):
    queryset = Admission.objects.all()
    
    def get_serializer_class(self, *args, **kwargs):
        return AdmissionSerializer