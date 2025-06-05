from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny
from drf_spectacular.utils import extend_schema


# 🔐 Serializer for Registration
class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["email", "password"]

    def create(self, validated_data):
        email = validated_data["email"]
        password = validated_data["password"]

        # 👇 Create user with email as both email and username
        user = User.objects.create_user(
            username=email,  # 🔐 Required by Django's default User model
            email=email,
            password=password,
        )
        user.is_active = True  # Optional, but good to ensure
        user.save()
        return user


# 🔐 API View for Registration
class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        request=RegisterSerializer,
        responses={201: None},
        description="Register a new user with email and password",
    )
    def post(self, request):
        print("RegisterView POST request received")
        serializer = RegisterSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "User registered successfully"},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
