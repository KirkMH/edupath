# pyrefly: ignore [missing-import]
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from customization.models import AptitudeQuestion
from .models import StudentProfile, StudentAptitudeResponse, StudentInterestResponse
from .services import sync_interest_questions


def index(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('/admin/')
        return redirect('dashboard')

    return render(request, 'index.html')


def signup(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('/admin/')
        return redirect('dashboard')

    if request.method == 'POST':
        full_name = request.POST.get('fullName', '').strip()
        student_id = request.POST.get('studentId', '').strip()
        age_raw = request.POST.get('age', '').strip()
        sex = request.POST.get('sex', '').strip()
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirmPassword', '')
        security_question = request.POST.get('securityQuestion', '').strip()
        security_answer = request.POST.get('securityAnswer', '').strip()
        terms = request.POST.get('terms')

        errors = []

        # 1. Validate required fields (Email is optional!)
        if not full_name:
            errors.append("Full Name is required.")
        if not student_id:
            errors.append("Student ID / LRN is required.")
        elif not student_id.isdigit() or len(student_id) != 12:
            errors.append("Student ID / LRN must be exactly a 12-digit number.")
        if not age_raw:
            errors.append("Age is required.")
        if not sex:
            errors.append("Sex is required.")
        if not password:
            errors.append("Password is required.")
        if not security_question:
            errors.append("Security question is required.")
        if not security_answer:
            errors.append("Security answer is required.")

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
            return render(request, 'signup.html', {
                'errors': errors,
                'form_data': {
                    'fullName': full_name,
                    'studentId': student_id,
                    'age': age_raw,
                    'sex': sex,
                    'email': email,
                    'securityQuestion': security_question,
                    'securityAnswer': security_answer,
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
                sex=sex,
                security_question=security_question,
                security_answer=security_answer
            )

            # Log in the user and redirect to dashboard
            login(request, user)
            return redirect('dashboard')
        except IntegrityError:
            errors.append("An error occurred while creating your account. Please verify your information and try again.")
            return render(request, 'signup.html', {
                'errors': errors,
                'form_data': {
                    'fullName': full_name,
                    'studentId': student_id,
                    'age': age_raw,
                    'sex': sex,
                    'email': email,
                    'securityQuestion': security_question,
                    'securityAnswer': security_answer,
                }
            })

    return render(request, 'signup.html')


def signin(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('/admin/')
        return redirect('dashboard')

    success = None
    if request.GET.get('reset') == 'success':
        success = "Password updated successfully! Please sign in with your new password."

    if request.method == 'POST':
        login_id = request.POST.get('login_id', request.POST.get('username', request.POST.get('email', ''))).strip()
        password = request.POST.get('password', '')
        remember_me = request.POST.get('rememberMe')

        if not login_id or not password:
            return render(request, 'signin.html', {
                'error': 'Please provide your Username, Student ID, or Email and password.',
                'login_id': login_id,
                'success': success,
            })

        # Find user by username (student_id / admin username) or email
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

            if user.is_staff or user.is_superuser:
                next_url = request.GET.get('next') or request.POST.get('next') or '/admin/'
                return redirect(next_url)
            else:
                next_url = request.GET.get('next') or request.POST.get('next') or 'dashboard'
                if next_url.startswith('/admin'):
                    next_url = 'dashboard'
                return redirect(next_url)
        else:
            return render(request, 'signin.html', {
                'error': 'Invalid Username/Student ID/Email address or password.',
                'login_id': login_id,
                'success': success,
            })

    return render(request, 'signin.html', {'success': success})


def forgot_password(request):
    if request.user.is_authenticated:
        if request.user.is_staff or request.user.is_superuser:
            return redirect('/admin/')
        return redirect('dashboard')

    error = None
    step = 1
    form_data = {}

    if request.method == 'POST':
        action_step = request.POST.get('step', '1')

        if action_step == '1':
            student_id = request.POST.get('studentId', '').strip()
            security_question = request.POST.get('securityQuestion', '').strip()
            security_answer = request.POST.get('securityAnswer', '').strip()

            form_data = {
                'studentId': student_id,
                'securityQuestion': security_question,
                'securityAnswer': security_answer,
            }

            if not student_id:
                error = "Learner's Reference Number (LRN) is required."
            elif not student_id.isdigit() or len(student_id) != 12:
                error = "Learner's Reference Number (LRN) must be exactly a 12-digit number."
            elif not security_question:
                error = "Please select your security question."
            elif not security_answer:
                error = "Security answer is required."
            else:
                try:
                    profile = StudentProfile.objects.get(student_id__iexact=student_id)
                    if (profile.security_question == security_question and
                        profile.security_answer and
                        profile.security_answer.strip().lower() == security_answer.strip().lower()):
                        # Verification successful! Advance to Step 2.
                        request.session['reset_student_id'] = profile.student_id
                        step = 2
                    else:
                        error = "The security question or answer does not match our records."
                except StudentProfile.DoesNotExist:
                    error = "No student account found with the provided LRN."

        elif action_step == '2':
            reset_student_id = request.session.get('reset_student_id')
            if not reset_student_id:
                error = "Session expired or invalid verification state. Please verify your details again."
                step = 1
            else:
                password = request.POST.get('password', '')
                confirm_password = request.POST.get('confirmPassword', '')

                if not password:
                    error = "New password is required."
                    step = 2
                elif not confirm_password:
                    error = "Please re-enter your new password."
                    step = 2
                elif password != confirm_password:
                    error = "Passwords do not match."
                    step = 2
                else:
                    try:
                        profile = StudentProfile.objects.get(student_id=reset_student_id)
                        user = profile.user
                        user.set_password(password)
                        user.save()

                        if 'reset_student_id' in request.session:
                            del request.session['reset_student_id']

                        return redirect('/signin/?reset=success')
                    except (StudentProfile.DoesNotExist, User.DoesNotExist):
                        error = "User account not found. Please try again."
                        step = 1

    return render(request, 'forgot_password.html', {
        'error': error,
        'step': step,
        'form_data': form_data,
        'student_id': request.session.get('reset_student_id', '') if step == 2 else ''
    })



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
    student_profile = request.user.student_profile
    questions = sync_interest_questions()

    if request.method == 'POST':
        for question in questions:
            rating_val = request.POST.get(f'q_{question.question_id}')
            if rating_val and rating_val.isdigit():
                rating_int = int(rating_val)
                if 1 <= rating_int <= 5:
                    StudentInterestResponse.objects.update_or_create(
                        student=student_profile,
                        question=question,
                        defaults={'rating': rating_int}
                    )
        student_profile.last_date_taken = timezone.now()
        student_profile.save()
        return redirect('loading')

    existing_responses = StudentInterestResponse.objects.filter(student=student_profile)
    user_answers = {resp.question_id: resp.rating for resp in existing_responses}

    import json
    return render(request, 'assessment/preference-assess.html', {
        'questions': questions,
        'user_answers': user_answers,
        'user_answers_json': json.dumps(user_answers),
        'total_questions': len(questions) or 60,
    })


@login_required(login_url='signin')
def loading(request):
    return render(request, 'assessment/loading.html')


@login_required(login_url='signin')
def result(request):
    return render(request, 'assessment/result.html')


