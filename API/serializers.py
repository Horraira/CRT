from rest_framework import serializers
from Auth.models import CustomUser
from .models import (
    Resume,
    PersonalInfo,
    Experience,
    Education,
    Skill,
    Summary,
    Certification,
)


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = ["id", "title", "created_at", "updated_at", "is_active"]
        read_only_fields = ["created_at", "updated_at"]

    def create(self, validated_data):
        validated_data["user"] = self.context["request"].user
        return super().create(validated_data)


class PersonalInfoSerializer(serializers.ModelSerializer):
    profile_picture_url = serializers.SerializerMethodField()

    class Meta:
        model = PersonalInfo
        fields = "__all__"
        read_only_fields = ["user", "profile_picture_url"]

    def get_profile_picture_url(self, obj):
        if obj.profile_picture:
            return self.context["request"].build_absolute_uri(obj.profile_picture.url)
        return None


class ExperienceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Experience
        fields = "__all__"
        read_only_fields = ["user"]

    def validate(self, data):
        if not data.get("is_current") and not data.get("endDate"):
            raise serializers.ValidationError(
                {"endDate": "End date is required if not current position"}
            )
        return data


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Education
        fields = "__all__"
        read_only_fields = ["user"]

    def validate(self, data):
        if not data.get("isCurrent") and not data.get("endDate"):
            raise serializers.ValidationError(
                {"endDate": "End date is required if not current education"}
            )
        return data


class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = "__all__"
        read_only_fields = ["user"]


class SummarySerializer(serializers.ModelSerializer):
    class Meta:
        model = Summary
        fields = ["id", "user", "content", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at", "user"]


class CertificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Certification
        fields = [
            "id",
            "name",
            "issuer",
            "date_obtained",
            "expiry_date",
            "credential_id",
            "credential_url",
        ]


# Nested Serializers for detailed views
class ResumeDetailSerializer(serializers.ModelSerializer):
    personal_info = PersonalInfoSerializer(read_only=True)
    experiences = ExperienceSerializer(many=True, read_only=True)
    educations = EducationSerializer(many=True, read_only=True)
    skills = SkillSerializer(many=True, read_only=True)
    summary = SummarySerializer(read_only=True)
    certifications = CertificationSerializer(many=True, read_only=True)

    class Meta:
        model = Resume
        fields = [
            "id",
            "title",
            "created_at",
            "updated_at",
            "is_active",
            "personal_info",
            "experiences",
            "educations",
            "skills",
            "summary",
            "certifications",
        ]
        read_only_fields = ["created_at", "updated_at"]


class UserInfoSerializer(serializers.ModelSerializer):
    personal_info = PersonalInfoSerializer(read_only=True)
    experience = ExperienceSerializer(many=True, read_only=True, source="experiences")
    education = EducationSerializer(many=True, read_only=True, source="educations")
    skills = SkillSerializer(many=True, read_only=True)
    summary = SummarySerializer(read_only=True, source="user_summary")

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "email",
            "personal_info",
            "experience",
            "education",
            "skills",
            "summary",
        ]
