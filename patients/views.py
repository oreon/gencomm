import datetime
import json
import sys

from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.urlresolvers import reverse_lazy
from django.shortcuts import render, render_to_response
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.template.defaulttags import now
from django.views.generic.detail import DetailView
from django.views.generic.edit import UpdateView, CreateView, DeleteView
from django.views.generic.list import ListView
from django_tables2.config import RequestConfig
from rest_framework import viewsets, status, permissions
from rest_framework.decorators import detail_route, list_route
from rest_framework.response import Response

from commerce.views import BaseViewSet, MultiSerializerViewSetMixin
import django_tables2 as tables
from patients.models import Bed, Patient, BedStay, Admission, Schedule, \
    PatientScheduleProcedure, Measurement
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
    
    def getData(self, request):
        data = json.loads(request.data)
        patientId = data['patient']
        note = data['note']
        return patientId, note
    
    @detail_route(methods=['put','post'])
    def admitPatient(self,request, *args, **kwargs):
        bed = self.get_object()
        try:
            
            patientId, note = self.getData(request)
            patient = Patient.objects.get(id = patientId)
    
            patient.admit(bed, request, note)
            
            bed.save()
            patient.save()
                   
            return Response( self.get_serializer(bed).data, status=status.HTTP_200_OK)
        except Exception as err:
            
            return Response(str(err),status=status.HTTP_400_BAD_REQUEST)

        
   

    @detail_route(methods=['put','post'])
    def transferPatient(self,request, *args, **kwargs):
        bed = self.get_object()
        try:
            
            patientId, note = self.getData(request)
            
            patient = Patient.objects.get(id = patientId)
            oldBed = patient.getBed()
            
            patient.transfer( bed, note)
            oldBed.vacate()  
                      
            oldBed.save()
            bed.save()
            patient.save()
            
            
            #self.movePatientIntoBed(request, bed, patient)
            
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
            
            patient.discharge(note)
            bed.vacate()
            
            bed.save()
            patient.save()
            
            assert(bed.patient == None)
            assert(patient.getBed() == None)
            return Response( 'discharged patient  from {0} '.format(bed.name), status=status.HTTP_200_OK)
        
        except Exception as err:
            return Response(str(err),status=status.HTTP_400_BAD_REQUEST)
        
             
        
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
    

class PatientScheduleProcedureTable(tables.Table):
    class Meta:
        model = PatientScheduleProcedure
        # add class="paleblue" to <table> tag
        attrs = {"class": "table"}
    
    
@staff_member_required
def patient_view(request, row_id): # Shows one row (all values in the object) in detail   
    
   
    #. . . create object of MyModel . . .
    pt = Patient.objects.get(id = row_id)   
    
    sptable = PatientScheduleProcedureTable(pt.scheduledProcedures.all())
    RequestConfig(request).configure(sptable)   
    return render(request , 'admin/patients/patient/viewPatient.html', {'patient': pt, 'sptable':sptable})
   
    
class MeasurementListView(LoginRequiredMixin,   ListView):
    model = Measurement
    paginate_by = 3
  #  filter_set = MeasurementFilter
    
    def get_context_data(self, **kwargs):
        context = super(MeasurementListView, self).get_context_data(**kwargs)
        context['current_request'] = self.request.META['QUERY_STRING']
        #context['form'] = ActorSearchForm()
        return context

class MeasurementUpdateView(LoginRequiredMixin, UpdateView):
    class Meta:
        model = Measurement
        fields = ('value', 'date', 'notes')
   
    
class MeasurementDetailView(LoginRequiredMixin, DetailView):
    model = Measurement
    # These next two lines tell the view to index lookups by username
    slug_field = "name"
    slug_url_kwarg = "name"
    
    
class PatientList(ListView):
    model = Patient

class PatientDetail(DetailView):
    model = Patient

class PatientCreate(CreateView):
    model = Patient
    fields = '__all__'

class PatientUpdate(UpdateView):
    model = Patient
    fields = '__all__'
    def get_success_url(self):
        return  reverse_lazy('patients:patient_detail', kwargs={'pk': self.object.id})

class PatientDelete(DeleteView):
    model = Patient
    success_url = reverse_lazy('patient_list')