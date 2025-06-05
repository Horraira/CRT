from rest_framework import serializers
from .models import TailoredCV

class TailoredCVSerializer(serializers.ModelSerializer):
    class Meta:
        model = TailoredCV
        fields = ['cv', 'job_description', 'tailored_json', 'created_at']
