from django.test import TestCase
from rest_framework import status

from commerce.tests import BaseTest


# Create your tests here.
class BedTests(BaseTest):
    
    url = 'beds'
    fixtures = ['users.yaml','patients.json']

        
    def test_getBedMap(self):
        response = self.client.get(self.url + '/getBedMap') 
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
    def test_admitPatient(self):
        pass


class PatientTests(BaseTest):
    
    url = 'patients'
    fixtures = ['users.yaml','patients.json']

        
    def test_createPatient(self):
        response = self.client.get(self.create_url())
        print(response.data)
        self.assertEqual(response.data['firstName']  ,'Jag')
        
    def test_admitPatient(self):
        response = self.client.put(self.create_url(suffix='admit') )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        #self.assertEqual(response.data['firstName']  ,'Jag')