from django import forms
from .models import JobPosting, Resume, Message
from django.contrib.auth.forms import UserCreationForm


class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['resume_file', 'skills', 'experience']

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['subject', 'message']
