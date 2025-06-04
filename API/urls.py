from django.urls import path
from .views import UploadCVJobView,CVJobResultView

urlpatterns = [
    path('upload/', UploadCVJobView.as_view(), name='upload-cv-job'),
    path('results/<int:pk>/', CVJobResultView.as_view(), name='cv-result'),
]
