from django.core.urlresolvers import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APITestCase

from commerce.models import Department, Employee


class QuestionMethodTests(TestCase):

    def testdisplayName(self):
        """
        was_published_recently() should return False for questions whose
        pub_date is in the future.
        """
        
        dep = Department(name='dba')
        self.assertEqual(dep.displayName, 'dba')


class DepartmentTests(APITestCase):
    
    url = 'http://localhost:8000/api/v1/departments'
    
    def setUp(self):
       self.create_department(self.client)
    
    def create_department(self, client):
        #self.url = reverse('departments')  TODO : 
        data = {'name': 'Dba'}
        response = client.post(self.url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response
    
    def test_create_department(self):
        self.assertEqual(Department.objects.count(), 1)
        self.assertEqual(Department.objects.get().displayName, 'Dba')
        print("created department {0}".format(Department.objects.get().id))
        
    def test_read_department(self):
        id = Department.objects.get().id
        print("found department {0}", id)
        url = self.url + "/" + str(id)
        response = self.client.get(url, format='json')
        self.assertEqual(response.data, {'id': 1, 'displayName': 'Dba', 'name': 'Dba'})
        
    def test_edit_department(self):
        
        id = Department.objects.get().id
        print("found department {0}", id)
        url = self.url + "/" + str(id)
        newdep = {'id': 1, 'displayName': 'Dba', 'name': 'DBA2'}
        response = self.client.put(url, newdep, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Department.objects.count(), 1)
        self.assertEqual(Department.objects.get().displayName, 'DBA2')
        
    
        
class EmployeeTests(APITestCase):
    
    url = 'http://localhost:8000/api/v1/employees'

    data =     {
            "department":1,
            "employeeSkills": [],
            #"displayName": "lomary, vivians",
            "gender": "MALE",
            "dob": "1988-11-05",
            "firstName": "lomary",
            "lastName": "vivians",
            "state": "hired"
        }
    
    def setUp(self):
        DepartmentTests().create_department(self.client)
        response = self.client.post(self.url, self.data, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        return response
    
    def create_url(self, recordid=1):
        return self.url + "/" + str(recordid)
    
    def read_employee(self, recordid=1):
        return self.client.get(self.create_url(recordid))
        #self.assertEqual(response.data['displayName'], 'lomary, vivians')
    
    def test_create_employee(self):
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual(Employee.objects.get(id=1 ).displayName, 'lomary, vivians')
        print("created emplolyee {0}".format(Employee.objects.get().id))
        
    def test_read_employee(self):
        response = self.read_employee()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['lastName'], 'vivians')
        
    def test_edit_employee(self):
        self.data['firstName'] = 'Mike'
        self.data['id'] = 1
        response = self.client.put(self.create_url(), self.data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual( Employee.objects.get(id=1  ).displayName,'Mike, vivians')
        
        
    def test_join_employee(self):
        response = self.client.put(self.create_url() + "/join", None, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual( Employee.objects.get(id=1  ).state,'active')
        
        
        
class EmployeeTestsFixture(APITestCase):
    
    url = 'http://localhost:8000/api/v1/employees'
    
    fixtures = ['testdata.yaml']

    data =     {
            "department":1,
            "employeeSkills": [],
            #"displayName": "lomary, vivians",
            "gender": "MALE",
            "dob": "1988-11-05",
            "firstName": "lomary",
            "lastName": "vivians",
            "state": "hired"
        }
    
    def create_url(self, recordid=1):
        return self.url + "/" + str(recordid)
    
    def read_employee(self, recordid=1):
        return self.client.get(self.create_url(recordid))
    
        
    def test_read_employee(self):
        response = self.read_employee()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['lastName'], 'vivians')
    
        
    def todo_edit_employee(self):
        self.data['firstName'] = 'Mike'
        self.data['id'] = 1
        response = self.client.put(self.create_url(), self.data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Employee.objects.count(), 1)
        self.assertEqual( Employee.objects.get(id=1).displayName,'Mike, vivians')