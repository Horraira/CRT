# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from .models import CV, JobDescription, TailoredCV
# from .serializers import TailoredCVSerializer
# import PyPDF2
# from django.core.files.storage import default_storage
# from .models import UploadedPDF


# class TailorCV(APIView):
#     def post(self, request):
#         # Step 1: Extract the file and job description from request
#         cv_file = request.FILES.get('cv_file')  # CV uploaded as file
#         job_desc = request.data.get('job_description')  # Job description sent as part of JSON

#         if not cv_file or not job_desc:
#             return Response({'error': 'CV file and job description are required.'}, status=status.HTTP_400_BAD_REQUEST)

#         # Step 2: Create and save the CV and JobDescription objects
#         cv = CV.objects.create(user=request.user, cv_file=cv_file)
#         job_description = JobDescription.objects.create(
#             title=request.data.get('job_title'),
#             description=job_desc,
#         )

#         # Step 3: Generate the tailored CV output (mock example for now)
#         tailored_output = self.tailor_cv(cv, job_description)

#         # Step 4: Save the tailored CV to the database
#         tailored_cv = TailoredCV.objects.create(
#             cv=cv,
#             job_description=job_description,
#             tailored_json=tailored_output,
#         )

#         # Return the tailored CV as a JSON response
#         serializer = TailoredCVSerializer(tailored_cv)
#         return Response(serializer.data, status=status.HTTP_200_OK)

#     def tailor_cv(self, cv, job_description):
#         """
#         This is where you would process the CV and tailor it based on the job description.
#         For now, it's a simple mock-up.
#         """
#         tailored_cv = {
#             "cv_user": cv.user.username,
#             "job_title": job_description.title,
#             "tailored_content": f"Tailored content for {cv.user.username} applying to {job_description.title}",
#         }
#         return tailored_cv


# class UploadPDF(APIView):
#     def post(self, request):
#         # Check if a PDF file is uploaded
#         pdf_file = request.FILES.get('pdf_file')

#         if not pdf_file:
#             return Response({"error": "PDF file is required."}, status=status.HTTP_400_BAD_REQUEST)

#         # Save the file (optional)
#         uploaded_pdf = UploadedPDF.objects.create(pdf_file=pdf_file)

#         # Extract text from the uploaded PDF
#         extracted_text = self.extract_pdf_text(pdf_file)

#         # Convert the extracted text to JSON
#         json_response = {"pdf_text": extracted_text}

#         return Response(json_response, status=status.HTTP_200_OK)

#     def extract_pdf_text(self, pdf_file):
#         """
#         This method extracts text from the provided PDF file.
#         """
#         # Open the PDF file
#         with pdf_file.open('rb') as file:
#             pdf_reader = PyPDF2.PdfReader(file)
#             text = ""
#             for page in pdf_reader.pages:
#                 text += page.extract_text() + "\n"
#         return text


import PyPDF2
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.core.files.storage import default_storage

class UploadPDF(APIView):
    def post(self, request):
        # Check if a PDF file is uploaded
        pdf_file = request.FILES.get('pdf_file')

        if not pdf_file:
            return Response({"error": "PDF file is required."}, status=status.HTTP_400_BAD_REQUEST)

        # Save the file to the default storage (optional)
        # uploaded_pdf = UploadedPDF.objects.create(pdf_file=pdf_file)

        # Extract text from the uploaded PDF
        extracted_text = self.extract_pdf_text(pdf_file)

        # Convert the extracted text to JSON
        json_response = {"pdf_text": extracted_text}

        return Response(json_response, status=status.HTTP_200_OK)

    def extract_pdf_text(self, pdf_file):
        """
        This method extracts text from the provided PDF file.
        """
        extracted_text = ""
        try:
            with pdf_file.open('rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    extracted_text += page.extract_text() + "\n"
        except Exception as e:
            return f"Error extracting text: {e}"
        return extracted_text
