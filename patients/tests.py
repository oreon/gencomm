from django.test import TestCase

from commerce.tests import BaseTest



# Create your tests here.
class PatientTests(BaseTest):
    
    url = 'patients'
    
    fixtures = ['users.yaml','patients.json']
    
    def setUp(self):
        self.login()
        self.url = self.baseurl + self.url
        
    def test_createPatient(self):
        response = self.client.get(self.create_url())
        print(response.data)
        self.assertEqual(response.data['firstName']  ,'Jag')
        
    def test_admitPatient(self):
        response = self.client.get(self.create_url(suffix='admit') )
        print(response.data)
        #self.assertEqual(response.data['firstName']  ,'Jag')