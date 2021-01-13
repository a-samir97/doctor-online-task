from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import (
    DoctorSessionsViewSetAPI,
    PatientBookSessionAPI,
    DisplayBookedSessionsAPI,
    DisplayAvailableSessionsAPI
)

router = DefaultRouter()
router.register('', DoctorSessionsViewSetAPI, basename='doctor-sessions')


urlpatterns = [
    path('book/<int:session_id>/', PatientBookSessionAPI.as_view(), name='book-session'),
    path('booked/', DisplayBookedSessionsAPI.as_view(), name='booked-sessions'),
    path('available/', DisplayAvailableSessionsAPI.as_view(), name='available-sessions'),

]

urlpatterns += router.urls