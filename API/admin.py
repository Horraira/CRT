from django.contrib import admin
from .models import (
    Resume,
    PersonalInfo,
    Experience,
    Education,
    Skill,
    Summary,
    Certification,
)

# Register your models here.


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    list_display = ("user", "jobTitle", "employer", "startDate", "endDate", "isCurrent")
    search_fields = ("user__username", "jobTitle", "employer")
    list_filter = ("isCurrent", "startDate", "endDate")
    ordering = ("-startDate",)


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    list_display = ("user", "degree", "school", "startDate", "endDate", "isCurrent")
    search_fields = ("user__username", "degree", "school")
    list_filter = ("isCurrent", "startDate", "endDate")
    ordering = ("-startDate",)


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("user", "skill", "proficiency")
    search_fields = ("user__username", "skill")
    list_filter = ("proficiency",)
    ordering = ("user", "skill")
