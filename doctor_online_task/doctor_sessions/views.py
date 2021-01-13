from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .models import DoctorSession
from .permissions import (
    IsDoctor, 
    IsPatient,
    IsOwner,
)

from .serializers import (
    SessionDetailSerializer, 
    SessionListSerializer
)

class DoctorSessionsViewSetAPI(ModelViewSet):
    '''
        ModelViewset for Doctor session 
        
            - doctors can create new session
            - doctors can delete existed session
            - doctors can get existed session
            - doctors can update existed session
    '''
    queryset = DoctorSession.objects.all()

    def get_permissions(self):

        if self.action == 'list' or self.action == 'retrieve':
            permission_classes = (IsAuthenticated,)

        elif self.action == 'create':
            permission_classes = (IsAuthenticated, IsDoctor)

        else:
            permission_classes = (IsAuthenticated, IsDoctor, IsOwner)
        
        return [permission() for permission in permission_classes]

    
    def get_serializer_class(self):
 
        if self.action == 'list' or self.action == 'retrieve':
            return SessionListSerializer
 
        else:
            return SessionDetailSerializer

    def perform_create(self, serializer):

        # save current user to doctor 
        serializer.save(doctor=self.request.user)

class PatientBookSessionAPI(APIView):

    permission_classes = (IsAuthenticated, IsPatient)
    def post(self, request, session_id):

        # check if session exists
        try:
            get_doctor_session = DoctorSession.objects.get(id=session_id)
        except DoctorSession.DoesNotExist:
            return Response(
                {'error': 'doctor session does not exist'},
                status=status.HTTP_404_NOT_FOUND
            )
        
        # check if the session has the same requested user
        if get_doctor_session.patient == request.user:
            return Response(
                {'error': 'you have already booked this session'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # check if the session has another patient 
        if get_doctor_session.patient != None and get_doctor_session.patient != request.user:
            return Response(
                {'error': 'this session is booked by another patient'},
                status=status.HTTP_400_BAD_REQUEST
            )

        get_doctor_session.patient = request.user
        get_doctor_session.save()

        return Response(
            {'data': 'you have booked successfully.'},
            status=status.HTTP_200_OK
        )

class DisplayBookedSessionsAPI(ListAPIView):
    queryset = DoctorSession.objects.filter(patient__isnull=False)
    serializer_class = SessionListSerializer
    permission_classes = (IsAuthenticated,)

class DisplayAvailableSessionsAPI(ListAPIView):
    queryset = DoctorSession.objects.filter(patient__isnull=True)
    serializer_class = SessionListSerializer
    permission_classes = (IsAuthenticated,)