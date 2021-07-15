import json
from django import http
from django.http import request, response
from django.test import client
from rest_framework import status
from rest_framework.test import APITestCase
from .models import User,Task
from django.urls import reverse
from .serializers import TaskSerializer
from django.test import TestCase
from rest_framework.test import APIClient

# # Create your tests here.
class RegistrationTestCase(APITestCase):
    def test_registration(self):
        data ={"email":"admind@gmail.com","password":"adsa","first_name":"bhuban","last_name":"ghimire"}
        response = self.client.post("/register/",data)
        self.assertEqual(response.status_code,status.HTTP_201_CREATED)
    
    
    def test_login(self):
        self.client.login(email="test@gmail.com", password="test")
        url = reverse('login')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK,'Expected Response Code 200, received {0} instead.'.format(response.status_code))


    

client = APIClient()
class TaskTestCase(APITestCase):
    def test_alltask(self):
        url = reverse('alltask')
        response = client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK,'Expected Response Code 200, received {0} instead.'.format(response.status_code))


    def test_task_by_id(self):
        url = reverse('task_by_id')
        data={"id":1}
        response = client.post(url,data,HTTP_AUTHORIZATION='')
        self.assertEqual(response.status_code, status.HTTP_200_OK,'Expected Response Code 200, received {0} instead.'.format(response.status_code))


    def test_task_by_status(self):
        url = reverse('task_by_status')
        response = self.client.post(url)
        # print(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK,'Expected Response Code 200, received {0} instead.'.format(response.status_code))


    def test_task_to_user(self):
        url = reverse('task_to_user')
        data = User.objects.create(email="asdjasj@gmail.com",first_name="bhuban",password="pass")
        token = "asdfljasdlksladfjsldjfsdklfj"
        response = client.get(url,headers={'Authorization': 'Bearer ' + token})
        self.assertEqual(response.status_code, status.HTTP_200_OK,'Expected Response Code 200, received {0} instead.'.format(response.status_code))

    

    def test_create_task(self):
        url = reverse('new_task')
        client = APIClient()
        token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjo4LCJ1c2VybmFtZSI6ImJodWJhbkBnbWFpbC5jb21zIiwiZXhwIjoxNjI2MzI5NDgzLCJlbWFpbCI6ImJodWJhbkBnbWFpbC5jb21zIn0.4Vdg33KlgSo8c_tgPwRt_gIhvfQD7y6mmmVgoqGmJr4"
        client.credentials(Authorization= 'Bearer ' + token)
       
        response = self.client.post(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    


