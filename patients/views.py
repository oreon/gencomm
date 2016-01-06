import sys

from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.decorators import detail_route
from rest_framework.response import Response

from commerce.views import BaseViewSet
from patients.models import Bed, Patient
from patients.serializers import BedSerializer, PatientSerializer


# Create your views here.
class BedViewSet( viewsets.ModelViewSet):
    queryset = Bed.objects.all()
    
    def get_serializer_class(self, *args, **kwargs):
        return BedSerializer
    
class PatientViewSet( BaseViewSet):
    queryset = Patient.objects.all()
    
    @detail_route(methods=['put','get'])
    def admit(self,request, *args, **kwargs):
        patient = self.get_object()
        try:
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