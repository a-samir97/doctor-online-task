from django.db import models

from users.models import User

class DoctorSession(models.Model):
    SESSIONS_TYPES = (
        ('W', 'Weekly Sessions'),
        ('D', 'One Day Sessions')
    )

    sessions_type = models.CharField(choices=SESSIONS_TYPES, max_length=1, default='D')
    title = models.CharField(max_length=30)
    price = models.IntegerField(default=0)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()

    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='booked_sessions', null=True, blank=True)