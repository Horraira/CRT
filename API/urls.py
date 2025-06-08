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
router.register(r"personal-info", PersonalInfoViewSet, basename="resume-personal-info")
router.register(r"experiences", ExperienceViewSet, basename="resume-experience")
router.register(r"educations", EducationViewSet, basename="resume-education")
router.register(r"skills", SkillViewSet, basename="resume-skill")
router.register(r"summary", SummaryViewSet, basename="resume-summary")
router.register(
    r"certifications", CertificationViewSet, basename="resume-certification"
)

urlpatterns = [
    path("", include(router.urls)),
]
