from rest_framework import serializers
from users.models import User

class SignupUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'},
        write_only=True,
        min_length=6
    )

    class Meta:
        model = User
        fields = ('username', 'password', 'first_name', 'last_name', 'user_type')
    

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User.objects.create(**validated_data)
        user.set_password(password)
        user.save()
        return user
