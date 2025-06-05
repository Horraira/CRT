from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.models import User
from rest_framework import serializers

class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD  # officially supported by DRF-SimpleJWT

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email:
            raise serializers.ValidationError({"email": "This field is required."})
        if not password:
            raise serializers.ValidationError({"password": "This field is required."})

        # Set 'username' key so parent validate() works
        attrs["username"] = email

        # Let the parent do the token stuff
        data = super().validate(attrs)

        # Add user info to response
        data["user_id"] = self.user.id
        data["email"] = self.user.email

        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        return token
