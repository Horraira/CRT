# from django.db import models

# class CV(models.Model):
#     user = models.ForeignKey('auth.User', on_delete=models.CASCADE)  # Foreign key to the User model
#     cv_file = models.FileField(upload_to='cv_files/')  # Store the uploaded CV
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"CV of {self.user.username} uploaded on {self.created_at}"


# class JobDescription(models.Model):
#     title = models.CharField(max_length=255)
#     description = models.TextField()  # Job description text
#     keywords = models.TextField(blank=True, null=True)  # Extracted keywords for matching
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Job Description: {self.title}"


# class TailoredCV(models.Model):
#     cv = models.ForeignKey(CV, on_delete=models.CASCADE)
#     job_description = models.ForeignKey(JobDescription, on_delete=models.CASCADE)
#     tailored_json = models.JSONField()  # Store the output as a JSON object
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Tailored CV for {self.cv.user.username} based on {self.job_description.title}"


# class UploadedPDF(models.Model):
#     pdf_file = models.FileField(upload_to='uploaded_pdfs/')
#     created_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"PDF uploaded on {self.created_at}"

from django.db import models

class UploadedPDF(models.Model):
    pdf_file = models.FileField(upload_to='uploaded_pdfs/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"PDF uploaded on {self.created_at}"
