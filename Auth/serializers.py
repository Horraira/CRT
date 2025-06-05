from django.contrib.auth.models import User
from rest_framework import serializers
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password']

    def create(self, validated_data):
        email = validated_data['email']
        password = validated_data['password']

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "A user with this email already exists."})

        if len(password) < 6:
            raise serializers.ValidationError({"password": "Password must be at least 6 characters long."})

        user = User.objects.create_user(
            username=email,  # Set email as username
            email=email,
            password=password
        )
        user.is_active = True  # Optional
        user.save()
        return user



class EmailTokenObtainPairSerializer(TokenObtainPairSerializer):
    username_field = User.EMAIL_FIELD  # Uses email as username

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        if not email:
            raise serializers.ValidationError({"email": "This field is required."})
        if not password:
            raise serializers.ValidationError({"password": "This field is required."})

        # Check if user exists
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "No account found with this email."})

        # Required by SimpleJWT under the hood
        attrs["username"] = email

        try:
            return super().validate(attrs)
        except serializers.ValidationError:
            raise serializers.ValidationError({"password": "Incorrect password."})

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        return token
