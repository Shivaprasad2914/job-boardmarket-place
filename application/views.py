# Create your views here.
from django.shortcuts import render, redirect
from .models import JobPosting, Resume, Message,UserRole
from .forms import  ResumeForm, MessageForm

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
# Home Page View
def home(request):
    job_postings = JobPosting.objects.all()
    return render(request, 'index.html', {'job_postings': job_postings})

# Job Seeker Dashboard
def job_seeker_dashboard(request):
    job_postings = JobPosting.objects.all()
    return render(request,'job_seeker_dashboard.html', {'job_postings': job_postings})

# Job Posting Form (For Employers)
def job_posting_form(request):
    if request.method == 'POST':
        # Retrieve form data from the POST request
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        salary = request.POST.get('salary')
        job_type = request.POST.get('job_type')
        skills_required = request.POST.get('skills_required')
        interview=request.POST.get('Interview')
        job_posting = JobPosting(
                title=title,
                description=description,
                location=location,
                salary=salary,
                job_type=job_type,
                skills_required=skills_required,
                employer=request.user,
                Interview_date=interview
            )
        job_posting.save()
        messages.success(request, "Job posted successfully!")
        return redirect('home')
    return render(request, 'job_posting_form.html')

# Message Form (For Communication)
# views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Message

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Save the message to the database
        if name and email and subject and message:
            data=Message.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message
            )
            data.save()
            messages.success(request, 'Your message has been sent successfully.')
            return redirect('send_message')  # Redirect back to the contact page
        else:
            messages.error(request, 'Please fill in all fields.')
    return render(request, 'contact_support.html')
# Custom Login View (Using Django's AuthenticationForm)
def custom_login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)  # Log the user in
            messages.success(request, f"Welcome, {user.username}!")
            return redirect('home')  # Redirect to home or any page after login
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()
    
    return render(request, 'login.html', {'form': form})

from django.contrib.auth.models import User

def register(request):
    if request.method == "POST":
        # Retrieve data from the POST request
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        is_employer = request.POST.get('is_employer')
        if is_employer=='employee':
            is_staff=True
        else:
            is_staff=False
        if password1 != password2:
            messages.error(request, "Passwords do not match.")
            return redirect('register')
        else:
            user=User.objects.filter(username=username)
            if user:
                messages.error(request, "username already exist")
                return redirect('register')
            else:
                user=User.objects.create_user(
                    username=username,
                    email=email,
                    password=password1,
                    is_staff=is_staff
                )
                user.save()
                login(request, user)
                if is_employer == 'on':  # Checkbox is either checked or not, so it will be 'on' if checked
                    UserRole.objects.create(user=user, is_employer=True, is_job_seeker=False)
                else:
                    UserRole.objects.create(user=user, is_employer=False, is_job_seeker=True)   
                    messages.success(request, "Registration successful. You are now logged in!")
            return redirect('home')
    return render(request,'register.html')
def logout_view(request):
    logout(request)
    return redirect('home')

from django.db.models import Q

def job_search(request):
    search=None
    query_params = request.GET  # Get query parameters from the URL (e.g., ?location=NY&job_type=Full-time)
    
    jobs = JobPosting.objects.all()
    
    # Apply filters based on the query parameters
    if 'location' in query_params:
        search=True
        jobs = jobs.filter(location__icontains=query_params['location'])
    if 'job_type' in query_params:
        search=True
        jobs = jobs.filter(job_type__icontains=query_params['job_type'])
    if 'skills' in query_params:
        search=True
        jobs = jobs.filter(skills_required__icontains=query_params['skills'])

    return render(request, 'Searchpage.html', {'jobs': jobs,'search':search})
@login_required
def manage_resume(request):
    try:
        # Check if the user has an existing resume
        resume = Resume.objects.get(user=request.user)
        if request.method == 'POST':
            # If resume exists, update it with the new data
            resume.skills = request.POST.get('skills')
            resume.experience = request.POST.get('experience')
            
            # Handle file upload
            if 'resume_file' in request.FILES:
                resume.resume_file = request.FILES['resume_file']
            resume.save()

            messages.success(request, "Resume updated successfully.")
            return redirect('view_resume')
        else:
            return render(request, 'manage_resume.html', {'resume': resume, 'is_update': True})
    
    except Resume.DoesNotExist:
        if request.method == 'POST':
            # If no resume exists, create one
            skills = request.POST.get('skills')
            experience = request.POST.get('experience')
            resume_file = request.FILES.get('resume_file')
            
            resume = Resume(user=request.user, skills=skills, experience=experience, resume_file=resume_file)
            resume.save()

            messages.success(request, "Resume created successfully.")
            return redirect('view_resume')
        else:
            return render(request, 'manage_resume.html', {'is_update': False})

@login_required
def view_resume(request):
    try:
        resume = Resume.objects.get(user=request.user)
        return render(request, 'view_resume.html', {'resume': resume})
    except Resume.DoesNotExist:
        messages.error(request, "No resume found. Please create one.")
        return redirect('manage_resume')