from django.db import models
from Auth.models import CustomUser
from django.core.validators import MinLengthValidator
from django.core.exceptions import ValidationError


class Resume(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name="resumes"
    )
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["-updated_at"]

    def __str__(self):
        return f"{self.user.email}'s {self.title}"


class PersonalInfo(models.Model):
    resume = models.OneToOneField(
        Resume, on_delete=models.CASCADE, related_name="personal_info"
    )
    first_name = models.CharField(max_length=50, validators=[MinLengthValidator(3)])
    last_name = models.CharField(max_length=50, validators=[MinLengthValidator(3)])
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True)
    location = models.CharField(max_length=100, blank=True)
    linkedin = models.URLField(blank=True)
    website = models.URLField(blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Experience(models.Model):
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="experiences"
    )
    company = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField()
    location = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["-start_date"]

    def clean(self):
        if not self.is_current and not self.end_date:
            raise ValidationError("End date is required if not current position")

    def __str__(self):
        return f"{self.position} at {self.company}"


class Education(models.Model):
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="educations"
    )
    school = models.CharField(max_length=100)
    degree = models.CharField(max_length=100)
    field = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    is_current = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=100, blank=True)

    class Meta:
        ordering = ["-start_date"]

    def clean(self):
        if not self.is_current and not self.end_date:
            raise ValidationError("End date is required if not current education")

    def __str__(self):
        return f"{self.degree} in {self.field} at {self.school}"


class Skill(models.Model):
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, related_name="skills")
    name = models.CharField(max_length=50)
    level = models.CharField(
        max_length=20,
        choices=[
            ("beginner", "Beginner"),
            ("intermediate", "Intermediate"),
            ("advanced", "Advanced"),
            ("expert", "Expert"),
        ],
    )
    category = models.CharField(max_length=50, blank=True)

    class Meta:
        unique_together = ["resume", "name"]

    def __str__(self):
        return f"{self.name} ({self.level})"


class Summary(models.Model):
    resume = models.OneToOneField(
        Resume, on_delete=models.CASCADE, related_name="summary"
    )
    content = models.TextField(validators=[MinLengthValidator(50)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Summary for {self.resume.title}"


class Certification(models.Model):
    resume = models.ForeignKey(
        Resume, on_delete=models.CASCADE, related_name="certifications"
    )
    name = models.CharField(max_length=100)
    issuer = models.CharField(max_length=100)
    date_obtained = models.DateField()
    expiry_date = models.DateField(null=True, blank=True)
    credential_id = models.CharField(max_length=100, blank=True)
    credential_url = models.URLField(blank=True)

    class Meta:
        ordering = ["-date_obtained"]

    def __str__(self):
        return f"{self.name} from {self.issuer}"
