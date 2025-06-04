from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import CVJobInputSerializer
from .models import CVJobInput
from .serializers import CVJobInputDetailSerializer
from rest_framework.generics import RetrieveAPIView

from drf_spectacular.utils import extend_schema

class UploadCVJobView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=CVJobInputSerializer,
        responses={201: None},
        description="Upload CV and job description",
    )
    def post(self, request, format=None):
        serializer = CVJobInputSerializer(data=request.data)
        if serializer.is_valid():
            instance = serializer.save(user=request.user)
            return Response({"message": "Upload successful", "id": instance.id}, status=201)
        return Response(serializer.errors, status=400)

class CVJobResultView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CVJobInput.objects.all()
    serializer_class = CVJobInputDetailSerializer

    def get_queryset(self):
        # Ensure users can only access their own uploads
        return CVJobInput.objects.filter(user=self.request.user)