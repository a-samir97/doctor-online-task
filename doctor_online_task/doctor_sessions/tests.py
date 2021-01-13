from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status

from users.models import User
from .models import DoctorSession

class DoctorSessionTests(APITestCase):

    def setUp(self):
        '''
            set up function
            create doctor and patient user types
        '''
        self.doctor = User.objects.create(
            username='doctor',
            password='doctordoctor',
            first_name='firstdoctor',
            last_name='lastdoctor',
            user_type='D'
        )

        self.patient = User.objects.create(
            username='patient',
            password='patientpatient',
            first_name='firstpatient',
            last_name='lastpatient',
            user_type='P'
        )

        self.create_session_url = '/api/sessions/'

    def test_create_session_with_valid_data(self):
        '''
            function to test creating doctor session with valid data 
        '''
        self.client.force_login(self.doctor)

        data ={
            'doctor':self.doctor.id,
            'title': 'first slot here',
            'price':10,
            'date':'2021-01-14',
            'start_time':'00:28:00',
            'end_time':'02:28:00',
            'sessions_type':'D'
        }

        response = self.client.post(self.create_session_url, data=data, format='json')
        
        # check of there is two user in database
        self.assertEqual(DoctorSession.objects.all().count(), 1)

        # check of the new user is created successfully
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
    
    def test_create_session_with_patient_user_type(self):
        self.client.force_login(self.patient)

        data ={
            'doctor':self.patient.id,
            'title': 'first slot here',
            'price':10,
            'date':'2021-01-14',
            'start_time':'00:28:00',
            'end_time':'02:28:00',
            'sessions_type':'D'
        }

        response = self.client.post(self.create_session_url, data=data, format='json')
        
        # check of there is two user in database
        self.assertEqual(DoctorSession.objects.all().count(), 0)

        # check of the new user is created successfully
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_session_with_invalid_data(self):
        self.client.force_login(self.doctor)

        data ={
            'doctor':self.doctor.id,
            'title': '',
            'price':10,
            'date':'2021-01-14',
            'start_time':'00:28:00',
            'end_time':'02:28:00',
            'sessions_type':'D'
        }

        response = self.client.post(self.create_session_url, data=data, format='json')
        
        # check of there is two user in database
        self.assertEqual(DoctorSession.objects.all().count(), 0)

        # check of the new user is created successfully
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class PatientBookSessionTests(APITestCase):
    def setUp(self):
        '''
            set up function
            create doctor and patient user types
        '''
        self.doctor = User.objects.create(
            username='doctor',
            password='doctordoctor',
            first_name='firstdoctor',
            last_name='lastdoctor',
            user_type='D'
        )

        self.patient = User.objects.create(
            username='patient',
            password='patientpatient',
            first_name='firstpatient',
            last_name='lastpatient',
            user_type='P'
        )
        self.patient_1 = User.objects.create(
            username='patient1',
            password='patientpatient1',
            first_name='firstpatient1',
            last_name='lastpatient1',
            user_type='P'
        )

        self.doctor_session = DoctorSession.objects.create(
            doctor=self.doctor,
            title='slot number 1',
            sessions_type='D',
            price=100,
            date='2021-01-14',
            start_time='00:28:00',
            end_time='02:28:00'
        )

        self.doctor_session_1 = DoctorSession.objects.create(
            doctor=self.doctor,
            title='slot number 1',
            sessions_type='D',
            price=100,
            date='2021-01-14',
            start_time='00:28:00',
            end_time='02:28:00',
            patient=self.patient
        )

        self.book_session = reverse('book-session', kwargs={'session_id':self.doctor_session.id})
        self.book_session_1 = reverse('book-session', kwargs={'session_id':self.doctor_session_1.id})

    def test_patient_book_doctor_session(self):

        # for login
        self.client.force_login(self.patient)

        response = self.client.post(self.book_session)

        # check of there is two user in database
        self.assertEqual(DoctorSession.objects.first().patient, self.patient)

        # check of the new user is created successfully
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_patient_book_with_already_booked_session(self):
        # for login
        self.client.force_login(self.patient_1)

        response = self.client.post(self.book_session_1)

        # check of there is two user in database
        self.assertEqual(DoctorSession.objects.last().patient, self.patient)

        # check of the new user is created successfully
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)