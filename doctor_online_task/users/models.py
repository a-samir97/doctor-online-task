from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE = (
        ('D', 'Doctor'),
        ('P', 'Patient')
    )

    user_type = models.CharField(choices=USER_TYPE, max_length=1)


    def __str__(self):
        return self.username