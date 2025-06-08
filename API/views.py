from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView
from resume_core import cvparser


from drf_spectacular.utils import extend_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import (
    Resume,
    PersonalInfo,
    Experience,
    Education,
    Skill,
    Summary,
    Certification,
)
from .serializers import (
    ResumeSerializer,
    ResumeDetailSerializer,
    PersonalInfoSerializer,
    ExperienceSerializer,
    EducationSerializer,
    SkillSerializer,
    SummarySerializer,
    CertificationSerializer,
)


class ResumeViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ResumeSerializer

    def get_queryset(self):
        return Resume.objects.filter(user=self.request.user)

    def get_serializer_class(self):
        if self.action == "retrieve":
            return ResumeDetailSerializer
        return ResumeSerializer

    @extend_schema(responses={200: ResumeDetailSerializer})
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class PersonalInfoViewSet(viewsets.ModelViewSet):
    queryset = PersonalInfo.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = PersonalInfoSerializer


class ExperienceViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = ExperienceSerializer

    def get_queryset(self):
        resume_id = self.kwargs.get("resume_pk")
        return Experience.objects.filter(
            resume_id=resume_id, resume__user=self.request.user
        )

    def perform_create(self, serializer):
        resume = get_object_or_404(
            Resume, id=self.kwargs.get("resume_pk"), user=self.request.user
        )
        serializer.save(resume=resume)


class EducationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = EducationSerializer

    def get_queryset(self):
        resume_id = self.kwargs.get("resume_pk")
        return Education.objects.filter(
            resume_id=resume_id, resume__user=self.request.user
        )

    def perform_create(self, serializer):
        resume = get_object_or_404(
            Resume, id=self.kwargs.get("resume_pk"), user=self.request.user
        )
        serializer.save(resume=resume)


class SkillViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SkillSerializer

    def get_queryset(self):
        resume_id = self.kwargs.get("resume_pk")
        return Skill.objects.filter(resume_id=resume_id, resume__user=self.request.user)

    def perform_create(self, serializer):
        resume = get_object_or_404(
            Resume, id=self.kwargs.get("resume_pk"), user=self.request.user
        )
        serializer.save(resume=resume)


class SummaryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = SummarySerializer

    def get_queryset(self):
        resume_id = self.kwargs.get("resume_pk")
        return Summary.objects.filter(
            resume_id=resume_id, resume__user=self.request.user
        )

    def perform_create(self, serializer):
        resume = get_object_or_404(
            Resume, id=self.kwargs.get("resume_pk"), user=self.request.user
        )
        serializer.save(resume=resume)


class CertificationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = CertificationSerializer

    def get_queryset(self):
        resume_id = self.kwargs.get("resume_pk")
        return Certification.objects.filter(
            resume_id=resume_id, resume__user=self.request.user
        )

    def perform_create(self, serializer):
        resume = get_object_or_404(
            Resume, id=self.kwargs.get("resume_pk"), user=self.request.user
        )
        serializer.save(resume=resume)
