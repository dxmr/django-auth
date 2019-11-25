from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from users.models import CustomUser


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(max_length=10)
    last_name = serializers.CharField(max_length=10)
    email = serializers.EmailField(
        required=True,
    )
    password = serializers.CharField(min_length=8, write_only=True)

    def create(self, validated_data):
        user = CustomUser.objects.create_user(**validated_data)
        return user

    class Meta:
        model = CustomUser
        fields = ('first_name', 'last_name', 'email', 'password')
