
from django.db import models
from django.contrib.auth.models import User
# Custom User Model
class UserRole(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    is_employer = models.BooleanField(default=False)
    is_job_seeker = models.BooleanField(default=False)

# Job Posting Model
class JobPosting(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    employer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posted_jobs')
    location = models.CharField(max_length=100)
    salary = models.IntegerField(null=True, blank=True)
    job_type = models.CharField(max_length=50)
    Interview_date=models.DateField(auto_now_add=False,blank=True)
    skills_required = models.TextField()
    date_posted = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# Resume Model
class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="resume")
    resume_file = models.FileField(upload_to="resumes/")
    skills = models.TextField()
    experience = models.TextField()

# Message Model
class Message(models.Model):
    name=models.CharField(max_length=20)
    email=models.EmailField()
    subject = models.CharField(max_length=255)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
