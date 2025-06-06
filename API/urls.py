from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ResumeViewSet,
    PersonalInfoViewSet,
    ExperienceViewSet,
    EducationViewSet,
    SkillViewSet,
    SummaryViewSet,
    CertificationViewSet,
)

router = DefaultRouter()
router.register(r"resumes", ResumeViewSet, basename="resume")

# Nested routers for resume-related endpoints
resume_router = DefaultRouter()
resume_router.register(
    r"personal-info", PersonalInfoViewSet, basename="resume-personal-info"
)
resume_router.register(r"experiences", ExperienceViewSet, basename="resume-experience")
resume_router.register(r"educations", EducationViewSet, basename="resume-education")
resume_router.register(r"skills", SkillViewSet, basename="resume-skill")
resume_router.register(r"summary", SummaryViewSet, basename="resume-summary")
resume_router.register(
    r"certifications", CertificationViewSet, basename="resume-certification"
)

urlpatterns = [
    path("", include(router.urls)),
    path("resumes/<int:resume_pk>/", include(resume_router.urls)),
]
