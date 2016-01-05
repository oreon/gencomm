from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from commerce.models import Department, Employee


class QuestionMethodTests(TestCase):

    def testdisplayName(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        
        dep = Department(name='dba')
        self.assertEqual(dep.displayName, 'dba')
        
empdata =     {
            "department":1,
            "employeeSkills": [],
            "gender": "MALE",
            "dob": "1988-11-05",
            "firstName": "lomary",
            "lastName": "vivians",
        }
        

class BaseTest(APITestCase):
    
    def login(self,usernm='jag'):
        self.client.logout()
        user = User.objects.get(username=usernm)
        self.client.force_authenticate(user=user)
        
    baseurl = 'http://localhost:8000/api/v1/'

    def create_url(self, recordid=1, suffix=None):
        suff = ''
        if (suffix):
            suff = "/" + suffix
        return self.url + "/" + str(recordid) + suff
    
    def read_one_record(self, recordid=1, suffix=None):
        return self.client.get(self.create_url(recordid, suffix))


class DepartmentTests(BaseTest):
    
    url = 'departments'
    
    fixtures = ['users.yaml','testdata.yaml']
    
    def setUp(self):
        self.login()
        self.url = self.baseurl + 'departments'
        
    def test_read_department(self):
        response = self.client.get(self.create_url(recordid=3))
        print(response.data)
        self.assertEqual(response.data['name']  ,'ITES')

    def test_edit_department(self):
        data = self.read_one_record(suffix='writable',recordid=3).data
        data['name'] = 'IT-2'
        response = self.client.put(self.create_url(recordid=3), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print(response.data)
        self.assertEqual(data['name'], 'IT-2')

    
    def test_create_department(self):
        data = self.read_one_record(suffix='writable',recordid=3).data
        data['id'] = None 
        response = self.client.post(self.url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
        
    def test_read_department_complete(self):
        self.client.post(self.baseurl + 'employees', empdata)
        response = self.client.get(self.create_url(suffix ='complete',recordid=3))
        self.assertEqual(len(response.data['employees'] ) ,4)
        

        
class EmployeeTests(BaseTest):
    
    url = 'http://localhost:8000/api/v1/employees'
    
    fixtures = ['users.yaml','testdata.yaml']
    
    def setUp(self):
        self.login()
        self.url = self.baseurl + 'employees'

        
    def test_read_employee(self):
        response = self.read_one_record()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['lastName'], 'vivians')
        self.assertEqual(response.data['department']['name'], 'ITES')
        
    def test_get_writable(self):
        response = self.read_one_record(suffix='writable')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['department'], 3) 
        
    def test_edit_employee(self):
        data = self.read_one_record(suffix='writable').data
        data['firstName'] = 'Mikey'
        response = self.client.put(self.create_url(), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual( Employee.objects.get(id=1).displayName,'Mikey, vivians')
        
    def test_create_employee(self):
        response = self.read_one_record(suffix='writable')
        data = response.data
        data['id'] = None
        response = self.client.post(self.url,data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)    
        
    def test_edit_employee_permission(self):
        self.login('alice');
        empdata['firstName'] = 'Jane'
        empdata['id'] = 1
        response = self.client.put(self.create_url(), empdata)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual( Employee.objects.get(id=1  ).displayName,'Mike, vivians')
    
    
    def test_join_employee(self):
        response = self.client.put(self.create_url() + "/join", None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual( Employee.objects.get(id=1).state,'active')
    
    def test_getAvailableStateTransitions_afterjoin(self):
        self.client.put(self.create_url() + "/join", None)
        response = self.client.get(self.create_url() + "/getAvailableStateTransitions", None)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, ["leave", "suspend"], "Incorrect states")
            