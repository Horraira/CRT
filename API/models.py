from django.db import models
from Auth.models import CustomUser


class CVJobInput(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cv_file = models.FileField(upload_to="uploads/cvs/", blank=False, null=False)
    job_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    processed = models.BooleanField(default=False)
    tailored_cv = models.FileField(upload_to="outputs/", null=True, blank=True)

    def __str__(self):
        return f"CVJobInput #{self.id} - {self.user.email}"
