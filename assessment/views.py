from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from customization.models import AptitudeQuestion
from .models import StudentProfile, StudentAptitudeResponse


def index(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        full_name = request.POST.get('fullName', '').strip()
        student_id = request.POST.get('studentId', '').strip()
        age_raw = request.POST.get('age', '').strip()
        sex = request.POST.get('sex', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirmPassword', '')
        terms = request.POST.get('terms')

        errors = []

        # 1. Validate required fields (Email is optional!)
        if not full_name:
            errors.append("Full Name is required.")
        if not student_id:
            errors.append("Student ID is required.")
        if not age_raw:
            errors.append("Age is required.")
        if not sex:
            errors.append("Sex is required.")
        if not password:
            errors.append("Password is required.")

        # 2. Checkbox validation
        if not terms:
            errors.append("You must agree to the Terms & Conditions and Privacy Policy.")

        # 3. Password matching validation
        if password and confirm_password and password != confirm_password:
            errors.append("Passwords do not match.")

        # 4. Optional email uniqueness validation
        if email and User.objects.filter(email__iexact=email).exclude(email='').exists():
            errors.append("An account with this email address is already registered.")

        # 5. Student ID uniqueness validation
        if student_id and StudentProfile.objects.filter(student_id__iexact=student_id).exists():
            errors.append("This Student ID is already registered.")

        # 6. Full Name and Student ID pair uniqueness validation
        if full_name and student_id and StudentProfile.objects.filter(full_name__iexact=full_name, student_id__iexact=student_id).exists():
            errors.append("A student profile with this Full Name and Student ID pair already exists.")

        if errors:
            return render(request, 'index.html', {
                'errors': errors,
                'form_data': {
                    'fullName': full_name,
                    'studentId': student_id,
                    'age': age_raw,
                    'sex': sex,
                    'email': email,
                }
            })

        # Parse age integer safely
        try:
            age = int(age_raw)
        except ValueError:
            age = None

        # Create Django User (username=student_id) & StudentProfile
        try:
            user = User.objects.create_user(
                username=student_id,
                email=email,
                password=password,
                first_name=full_name
            )
            StudentProfile.objects.create(
                user=user,
                student_id=student_id,
                full_name=full_name,
                age=age,
                sex=sex
            )

            # Log in the user and redirect to dashboard
            login(request, user)
            return redirect('dashboard')
        except IntegrityError:
            errors.append("An error occurred while creating your account. Please verify your information and try again.")
            return render(request, 'index.html', {
                'errors': errors,
                'form_data': {
                    'fullName': full_name,
                    'studentId': student_id,
                    'age': age_raw,
                    'sex': sex,
                    'email': email,
                }
            })

    return render(request, 'index.html')


def signin(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        login_id = request.POST.get('login_id', request.POST.get('email', '')).strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('rememberMe')

        if not login_id or not password:
            return render(request, 'signin.html', {
                'error': 'Please provide your Student ID or Email and password.',
                'login_id': login_id
            })

        # Find user by student_id (username) or email
        user_obj = None
        if User.objects.filter(username__iexact=login_id).exists():
            user_obj = User.objects.get(username__iexact=login_id)
        elif User.objects.filter(email__iexact=login_id).exclude(email='').exists():
            user_obj = User.objects.filter(email__iexact=login_id).exclude(email='').first()

        username_to_auth = user_obj.username if user_obj else login_id

        user = authenticate(request, username=username_to_auth, password=password)
        if user is not None:
            login(request, user)
            if remember_me:
                request.session.set_expiry(1209600)  # 2 weeks
            else:
                request.session.set_expiry(0)  # Expire on browser close
            next_url = request.GET.get('next', 'dashboard')
            return redirect(next_url)
        else:
            return render(request, 'signin.html', {
                'error': 'Invalid Student ID/Email address or password.',
                'login_id': login_id
            })

    return render(request, 'signin.html')


def signout(request):
    logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def dashboard(request):
    student_name = "Student"
    if request.user.is_authenticated:
        profile = getattr(request.user, 'student_profile', None)
        if profile and profile.full_name:
            student_name = profile.full_name
        elif request.user.first_name:
            student_name = request.user.first_name
        elif request.user.username:
            student_name = request.user.username

    if student_name:
        student_name = student_name.title()

    return render(request, 'assessment/dashboard.html', {
        'student_name': student_name
    })


@login_required(login_url='signin')
def aptitude_ready(request):
    return render(request, 'assessment/aptitude-ready.html')


@login_required(login_url='signin')
def assess_aptitude(request):
    student_profile = request.user.student_profile
    questions = AptitudeQuestion.objects.filter(status=True).order_by('question_id')

    if request.method == 'POST':
        for question in questions:
            selected_choice = request.POST.get(f'question_{question.question_id}')
            if selected_choice:
                is_correct = (selected_choice == question.correct_answer)
                StudentAptitudeResponse.objects.update_or_create(
                    student=student_profile,
                    question=question,
                    defaults={
                        'selected_answer': selected_choice,
                        'is_correct': is_correct
                    }
                )
        student_profile.last_date_taken = timezone.now()
        student_profile.save()
        return redirect('preference_ready')

    existing_responses = StudentAptitudeResponse.objects.filter(student=student_profile)
    user_answers = {resp.question_id: resp.selected_answer for resp in existing_responses}

    return render(request, 'assessment/aptitude-assess.html', {
        'questions': questions,
        'user_answers': user_answers,
    })


@login_required(login_url='signin')
def preference_ready(request):
    return render(request, 'assessment/preference-ready.html')


@login_required(login_url='signin')
def assess_preference(request):
    if request.method == 'POST':
        return redirect('result')
    return render(request, 'assessment/preference-assess.html')


@login_required(login_url='signin')
def result(request):
    return render(request, 'assessment/result.html')

