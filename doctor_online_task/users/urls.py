from django.urls import path 

from . import views

urlpatterns = [
    # Authentication URL
    path('signup/', views.SignupAPIView.as_view(), name='signup'),
    path('login/', views.LoginAPIView.as_view(), name='login'),
    
]