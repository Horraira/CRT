# Auth/serializers.py

from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']

        # Create user with email as both email and username
        user = User.objects.create_user(
            username=email,
            email=email,
            password=password
        )
        user.is_active = True  # Optional: ensure account is active
        user.save()
        return user
