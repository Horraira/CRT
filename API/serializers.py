from rest_framework import serializers
from .models import CVJobInput

class CVJobInputSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVJobInput
        fields = ['id', 'cv_file', 'job_description']
class CVJobInputDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = CVJobInput
        fields = ['id', 'cv_file', 'job_description', 'processed', 'tailored_cv', 'created_at']
