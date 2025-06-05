from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import CVJobInputSerializer, CVJobInputDetailSerializer
from .models import CVJobInput
from rest_framework.generics import RetrieveAPIView
from resume_core import cvparser


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
            # Step 1: Save the model instance
            instance = serializer.save(user=request.user)
            # Step 2: Access and read the uploaded PDF file
            cv_file = instance.cv_file

            # Read content (uploaded as InMemoryUploadedFile or TempFile)
            file_content = cv_file.read()

            # Step 3: Extract text using Jabed_Vi's parser
            try:
                extracted_text = cvparser.extract_text_from_pdf(file_content)
                parsed_data = cvparser.parse_resume_with_openai(extracted_text)
            except Exception as e:
                return Response({"error": str(e)}, status=500)

            # Step 4: Optionally store or return parsed_data
            return Response(
                {
                    "message": "Upload successful",
                    "id": instance.id,
                    "parsed_resume": parsed_data,
                },
                status=201,
            )

        return Response(serializer.errors, status=400)


class CVJobResultView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = CVJobInput.objects.all()
    serializer_class = CVJobInputDetailSerializer

    def get_queryset(self):
        return CVJobInput.objects.filter(user=self.request.user)
