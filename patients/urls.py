# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.conf.urls import url
from django.core.urlresolvers import reverse

from . import views


urlpatterns = [
    # URL pattern for the MeasurementListView    
    url(regex=r'^measurements-(?P<pm>[0-9]+)/$',view=views.MeasurementListView.as_view(),name='listMeasurements', ),
    url(regex=r'^measurements-(?P<pm>[0-9]+)/(?P<pk>[0-9]+)/update/$',view=views.MeasurementUpdateView.as_view(),name='updateMeasurement'),
    url(regex=r'^measurements-(?P<pm>[0-9]+)/create/$',view=views.MeasurementCreateView.as_view(),name='createMeasurement'),
    
 #   url(regex=r'^(?measurements/P<username>[\w.@+-]+)/$',view=views.MeasurementDetailView.as_view(),name='detail'),  
 
 url(r'^patients$',
        views.PatientList.as_view(),
        name='patient_list'),
    url(r'^patients/(?P<pk>[0-9]+)/$',
        views.PatientDetail.as_view(),
        name='patient_detail'),
    url(r'^patients/create$',
        views.PatientCreate.as_view(),
        name='patient_create'),
               
    url(r'^patients/(?P<pk>[0-9]+)/update/$',
        views.PatientUpdate.as_view(), 
        name='patient_edit'),
    url(r'^patients/(?P<pk>[0-9]+)/delete/$',
        views.PatientDelete.as_view(),
        name='patient_delete'),   
]