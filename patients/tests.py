import json

from django.test import TestCase
from rest_framework import status

from commerce.tests import BaseTest
from patients.models import Patient, Bed


# Create your tests here.
class BedTests(BaseTest):
    
    url = 'beds'
    fixtures = ['users.json','patients.json']
    
    def createDataForAdmission(self, pid):
        data = {'patient': pid, 'note' : "Admitting for further investigation "}
        return json.dumps(data)
    
    
    def admitPatient(self, pid = 1, bedid = 1):
        
        response = self.client.put(self.create_url(recordid= bedid , suffix='admitPatient'),  self.createDataForAdmission(pid))
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        patient = Patient.objects.get(id = pid)
        return patient    
    
        
    def test_getBedMap(self):
        response = self.client.get(self.url + '/getBedMap') 
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_admitPatient(self):
        patient = self.admitPatient()
        
        response = self.client.get(self.url + '/getBedMap')
        bed = list(filter( lambda x : x['bedId'] == 1, response.data))[0]
        self.assertEquals(bed['patient'] , patient.displayName)
        self.assertEquals(patient.getBed().id, 1)
        

        
    def test_AlreadyAdmittedPatient(self):
        patient = Patient.objects.get(id = 2)
        response = self.client.put(self.create_url(suffix='admitPatient' ),  self.createDataForAdmission(patient.id))
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    def test_AlreadyOccupiedBed(self):
        patient = Patient.objects.get(id = 1)
        self.assertEquals(patient.getBed(), None)
        response = self.client.put(self.create_url(recordid = 3, suffix='admitPatient'),  self.createDataForAdmission(patient.id))
        #print( response.data) #TODO 
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        

        
    def test_transferPatient(self):
        
        newbedId = 2
        
        patient = self.admitPatient()
        oldBedid = patient.getBed().id
        
        response = self.client.put(self.create_url(recordid=newbedId, suffix='transferPatient') , self.createDataForAdmission(patient.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        oldbed = Bed.objects.get(id = oldBedid)
        newbed = Bed.objects.get(id = newbedId)
        
        patient = Patient.objects.get(id = 1)
        
        self.assertEqual(patient.getBed().id, newbedId)
        self.assertEqual(oldbed.patient , None)
        self.assertEqual(newbed.patient, patient)
        
   
        
    def test_dischargePatient(self):
        
        newbedId = 2
        patient = self.admitPatient()
        
        bedid = patient.getBed().id
           
        response = self.client.put( self.create_url(recordid=newbedId, suffix='dischargePatient'), self.createDataForAdmission(patient.id)   )
        print(response.data)
        oldbed = Bed.objects.get(id = bedid)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        print(patient.getBed())
        
        patient = Patient.objects.get(id = 1)
        
        print(patient.getBed())
        self.assertEqual(oldbed.patient , None)
        self.assertEqual(patient.getBed(), None)
        
        self.assertEqual(oldbed.state, 'free')
        
        #admission


class PatientTests(BaseTest):
    
    url = 'patients'
    fixtures = ['users.json','patients.json']
        
    def test_readPatient(self):
        response = self.client.get(self.create_url())
        print(response.data)
        self.assertEqual(response.data['firstName']  ,'Jag')
        
    def test_createPatient(self):
        response = self.read_one_record(suffix='writable')
        data = response.data
        data['id'] = None
        data['user'] = 2
        response = self.client.post(self.url,data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        
        
    def t_admitPatient(self):
        response = self.client.put(self.create_url(suffix='admit?bed=2') )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        #self.assertEqual(response.data['firstName']  ,'Jag')
        
        
class ScheduleTests(BaseTest):
    
    url = 'schedules'
    
    fixtures = ['users.json','patients.json']
        
    def t_createScheduleByNurse(self):
        self.login('alicia-rn')
        response = self.read_one_record(suffix='writable')
        data = response.data
        data['id'] = None
        response = self.client.post(self.url,data)
        print(response.data)
        ''' access should be denied'''
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
    def test_createSchedule(self):
        #self.login('alicia-rn')
        response = self.read_one_record(suffix='writable')
        data = response.data
        data['id'] = None
        response = self.client.post(self.url,data)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        