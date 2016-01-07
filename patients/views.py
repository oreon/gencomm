import datetime
import sys

from django.shortcuts import render
from django.template.defaulttags import now
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from commerce.views import BaseViewSet
from patients.models import Bed, Patient, BedStay
from patients.serializers import BedSerializer, PatientSerializer


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
    
    @detail_route(methods=['put'])
    def admitPatient(self,request, *args, **kwargs):
        bed = self.get_object()
        try:
            patientId = request.query_params["patient"]
            patient = Patient.objects.get(id = patientId)
            
            patient.admit()
            
            self.movePatientIntoBed(bed, patient)
           
            return Response( 'admitted patient to {0} '.format(bed.name), status=status.HTTP_200_OK)
        except Exception as err:
            return Response(str(err),status=status.HTTP_400_BAD_REQUEST)

        
    @detail_route(methods=['put'])
    def transferPatient(self,request, *args, **kwargs):
        bed = self.get_object()
        try:
            patientId = request.query_params["patient"]
            patient = Patient.objects.get(id = patientId)
            oldBed = patient.getBed()
            
            patient.transfer()

            oldBed.vacate()
            #self.markBedStayEnd(bedStay)
            
            self.movePatientIntoBed(bed, patient)
            
            oldBed.save()
            return Response( 'transferred patient to {0} from {1} '.format(bed.name, oldBed.name), status=status.HTTP_200_OK)
        except Exception as err:
            return Response(str(err),status=status.HTTP_400_BAD_REQUEST)
        
    @detail_route(methods=['put'])
    def dischargePatient(self,request, *args, **kwargs):
        bed = self.get_object()
        try:
            patientId = request.query_params["patient"]
            patient = Patient.objects.get(id = patientId)
            bed = patient.getBed()
            
            patient.discharge()
            bed.vacate()
            
            bed.save()
            patient.save()
            
            #self.markBedStayEnd(bedStay)
            
            assert(bed.patient == None)
            return Response( 'discharged patient  from {0} '.format(bed.name), status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response(str(err),status=status.HTTP_400_BAD_REQUEST)
        
    def createBedStay(self, bed, patient):
        bedStay = BedStay()
        bedStay.bed = bed
        bedStay.patient = patient
        bedStay.startDate = datetime.date.today()
        #bedStay.save()
        
    def markBedStayEnd(self, bedStay):
        bedStay.endDate = now()
        bedStay.save()
        
    def movePatientIntoBed(self, bed, patient):
        assert(bed.patient == None)
        bed.occupy(patient)
        assert(bed.patient == patient)
        bed.save()
        patient.save()
        self.createBedStay(bed, patient)             
        
class PatientViewSet( BaseViewSet):
    queryset = Patient.objects.all()
    
    @detail_route(methods=['put'])
    def admit(self,request, *args, **kwargs):
        patient = self.get_object()
        try:
            bedid = request.get("bed")
            print(bedid)
            patient.admit()
            patient.bedId = 2
            bed = Bed.objects.get(id = patient.bedId)
            assert(bed.patient == None)
            bed.occupy(patient)
            assert(bed.patient == patient)
            patient.save()
            bed.save()
            return Response( 'admitted', status=status.HTTP_200_OK)
        except Exception as err:
            return Response(str(err),status=status.HTTP_400_BAD_REQUEST)
        
    
    def get_serializer_class(self, *args, **kwargs):
        return PatientSerializer