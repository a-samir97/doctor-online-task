from rest_framework import serializers
from .models import DoctorSession

class SessionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSession
        fields = '__all__'

class SessionDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = DoctorSession
        exclude = ('doctor' , 'patient')