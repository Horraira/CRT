# from django.urls import path
# from .views import TailorCV, UploadPDF

# urlpatterns = [
#     path('tailor-cv/', TailorCV.as_view(), name='tailor_cv'),  # Ensure this matches the endpoint you're trying to access
#     path('upload-pdf/', UploadPDF.as_view(), name='upload_pdf'),

# ]

# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('api/', include('cv_tailor.urls')),  # Include the cv_tailor URLs
# ]

from django.urls import path
from .views import UploadPDF

urlpatterns = [
    path('upload-pdf/', UploadPDF.as_view(), name='upload_pdf'),  # Route for uploading PDFs
]
