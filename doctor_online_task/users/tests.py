from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from .models import User

class UserRegisterTests(APITestCase):

    def setUp(self):
        '''
            Set up function for testing our code
        '''
        self.test_user = User.objects.create(
            username='testusername',
            email='test@test.com',
            password='testpassword',
        )

        self.create_signup_url = reverse('signup')
    

    def test_create_user(self):
        '''
        Creating user with valid data
        '''
        
        data = {
            'username': 'testtest',
            'password': 'testtestpassword',
            'first_name': 'test',
            'last_name': 'test',
            'user_type': 'D'
        }

        response = self.client.post(self.create_signup_url, data=data, format='json')

        # check of there is two user in database
        self.assertEqual(User.objects.all().count(), 2)

        # check of the new user is created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # check if username and email are correct
        self.assertEqual(response.data['username'], data['username'])
        self.assertEqual(response.data['user_type'], data['user_type'])
        self.assertEqual(response.data['first_name'], data['first_name'])
        self.assertEqual(response.data['last_name'], data['last_name'])
    
    
    def test_create_user_with_short_password(self):
        '''
        Ensure that user will not create password less than 8 chars
        '''

        data = {
            'username': 'testtest',
            'password': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'user_type': 'D'
        } 

        response = self.client.post(self.create_signup_url, data, format='json')

        # assert that status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # assert user will not be created
        self.assertEqual(User.objects.all().count(), 1)
    
    def test_create_user_with_no_password(self):
        """
        Ensure that user will not create empty password
        """

        data = {
            'username': 'testtest',
            'password': '',
            'first_name': 'test',
            'last_name': 'test',
            'user_type': 'D'
        } 

        response = self.client.post(self.create_signup_url, data, format='json')

        # assert that status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # assert user will not be created
        self.assertEqual(User.objects.all().count(), 1)

    
    def test_create_user_with_long_username(self):
        """
        Ensure that user will not input a very long username
        """
        data = {
            'username': 'testtest'*30,
            'password': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'user_type': 'D'
        } 

        response = self.client.post(self.create_signup_url, data, format='json')

        # assert that status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # assert user will not be created
        self.assertEqual(User.objects.all().count(), 1)
    
    def test_create_user_with_no_username(self):
        """
        Ensure that user will not input empty username
        """
        data = {
            'username': '',
            'password': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'user_type': 'D'
        } 

        response = self.client.post(self.create_signup_url, data, format='json')

        # assert that status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # assert user will not be created
        self.assertEqual(User.objects.all().count(), 1)

    
    def test_create_user_with_existing_username(self):

        """
        Ensure that user will not input existing username
        """
        data = {
            'username': 'testusername',
            'password': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'user_type': 'D'
        } 

        response = self.client.post(self.create_signup_url, data, format='json')

        # assert that status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # assert user will not be created
        self.assertEqual(User.objects.all().count(), 1)
 

    def test_create_user_with_wrong_email(self):
        """
        Ensure that user will not input invalid email
        """
        data = {
            'username': 'testusername',
            'password': 'test',
            'first_name': 'test',
            'last_name': 'test',
            'user_type': 'D'
        } 

        response = self.client.post(self.create_signup_url, data, format='json')

        # assert that status code is 400 BAD REQUEST
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # assert user will not be created
        self.assertEqual(User.objects.all().count(), 1) 



class UserLoginTests(APITestCase):

    def setUp(self):
        '''
            Set up function for testing our code
        '''
        self.test_user = User.objects.create_user(
            username='testusername',
            email='test@test.com',
            password='testpassword',
        )

        self.create_login_url = reverse('login')
    
    def test_login_user_with_valid_data(self):

        """
            Login user with valid data
        """

        data = {
            "username": "testusername",
            "password": "testpassword"
        }

        response = self.client.post(self.create_login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_login_user_with_no_username(self):
        """
            Ensure that user will not input empty username
        """

        data = {
            "username": "",
            "password": "testpassword"
        }

        response = self.client.post(self.create_login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_user_with_no_password(self):
        """
            Ensure that user will not input empty password
        """
        data = {
            "username": "testusername",
            "password": ""
        }

        response = self.client.post(self.create_login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_login_user_with_invalid_data(self):
        """
            Ensure that user will not pass invalid data while login
        """
        data = {
            "username": "username",
            "password": "password"
        }
        response = self.client.post(self.create_login_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)