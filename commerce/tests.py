from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from django.test import TestCase

from commerce.models import Department


class QuestionMethodTests(TestCase):

    def testdisplayName(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        
        dep = Department(name='dba')
        self.assertEqual(dep.displayName, 'dba')


class AccountTests(APITestCase):
    
    url = 'http://localhost:8000/api/v1/departments'
    
    def create_account(self):
        
        data = {'name': 'Dba'}
        response = self.client.post(self.url, data, format='json')
        return response
    
    def test_create_department(self):
        """
        Ensure we can create a new account object.
        """
        response = self.create_account();
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Department.objects.count(), 1)
        self.assertEqual(Department.objects.get().displayName, 'Dba')
        print("created department {0}".format(Department.objects.get().id))
        
    def test_read_department(self):
        
        response = self.create_account();
        id = Department.objects.get().id
        print("found department {0}", id)
        url = self.url + "/" + str(id)
        response = self.client.get(url, format='json')
        self.assertEqual(response.data, {'id': 1, 'displayName': 'Dba', 'name': 'Dba'})
        
    def test_edit_department(self):
        response = self.create_account();
        id = Department.objects.get().id
        print("found department {0}", id)
        url = self.url + "/" + str(id)
        newdep = {'id': 1, 'displayName': 'Dba', 'name': 'DBA2'}
        response = self.client.put(url, newdep, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Department.objects.count(), 1)
        self.assertEqual(Department.objects.get().displayName, 'DBA2')
        
    
        
        
        
        