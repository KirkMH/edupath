import random
from datetime import datetime, date
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.http import JsonResponse
from customization.models import AptitudeQuestion, ActivityLog, Program, check_and_lock_account
from .models import StudentProfile, StudentAptitudeResponse, StudentInterestResponse, AssessmentResult
from .services import (
    sync_interest_questions, calculate_and_save_assessment_results,
    lookup_score_interpretation, calculate_major_recommendations,
    calculate_program_recommendations
)
from django.shortcuts import render, redirect, get_object_or_404



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
        sex = request.POST.get('sex', '').strip()
        dob_raw = request.POST.get('dateOfBirth', '').strip() or request.POST.get('date_of_birth', '').strip() or request.POST.get('dob', '').strip()
        age_raw = request.POST.get('age', '').strip()
        gwa_raw = request.POST.get('gwa', '').strip()
        username = request.POST.get('username', '').strip()
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
        if not sex:
            errors.append("Sex is required.")
        if not dob_raw and not age_raw:
            errors.append("Date of Birth is required.")
        if not gwa_raw:
            errors.append("General Weighted Average (GWA) is required.")
        if not username:
            errors.append("Username is required.")
        if not password:
            errors.append("Password is required.")
        if not security_question:
            errors.append("Security question is required.")
        if not security_answer:
            errors.append("Security answer is required.")

        # Validate Date of Birth / Age
        date_of_birth = None
        age = None
        if dob_raw:
            try:
                date_of_birth = datetime.strptime(dob_raw, '%Y-%m-%d').date()
                today = timezone.localdate() if hasattr(timezone, 'localdate') else date.today()
                if date_of_birth > today:
                    errors.append("Date of Birth cannot be in the future.")
                else:
                    age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
                    if age < 5 or age > 120:
                        errors.append("Please enter a valid Date of Birth.")
            except ValueError:
                errors.append("Please enter a valid Date of Birth (YYYY-MM-DD).")
        elif age_raw:
            try:
                age = int(age_raw)
            except ValueError:
                age = None

        # Validate GWA numeric bounds
        gwa = None
        if gwa_raw:
            try:
                gwa = float(gwa_raw)
                if gwa < 50.0 or gwa > 100.0:
                    errors.append("General Weighted Average (GWA) must be between 50.00 and 100.00.")
            except ValueError:
                errors.append("Please enter a valid numeric General Weighted Average (GWA).")

        # 2. Checkbox validation
        if not terms:
            errors.append("You must agree to the Terms & Conditions and Privacy Policy.")

        # 3. Password matching validation
        if password and confirm_password and password != confirm_password:
            errors.append("Passwords do not match.")

        # 4. Optional email uniqueness validation
        if email and User.objects.filter(email__iexact=email).exclude(email='').exists():
            errors.append("An account with this email address is already registered.")

        # 5. Username uniqueness validation
        if username and (User.objects.filter(username__iexact=username).exists() or StudentProfile.objects.filter(username__iexact=username).exists()):
            errors.append("This Username is already registered.")

        # 6. Full Name and Username pair uniqueness validation
        if full_name and username and StudentProfile.objects.filter(full_name__iexact=full_name, username__iexact=username).exists():
            errors.append("A student profile with this Full Name and Username pair already exists.")

        if errors:
            return render(request, 'signup.html', {
                'errors': errors,
                'form_data': {
                    'fullName': full_name,
                    'sex': sex,
                    'dateOfBirth': dob_raw,
                    'age': age_raw,
                    'gwa': gwa_raw,
                    'username': username,
                    'email': email,
                    'securityQuestion': security_question,
                    'securityAnswer': security_answer,
                }
            })

        # Create Django User (username=username) & StudentProfile
        try:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=full_name
            )
            StudentProfile.objects.create(
                user=user,
                username=username,
                full_name=full_name,
                date_of_birth=date_of_birth,
                age=age,
                sex=sex,
                gwa=gwa,
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
                    'sex': sex,
                    'dateOfBirth': dob_raw,
                    'age': age_raw,
                    'gwa': gwa_raw,
                    'username': username,
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
                'error': 'Please provide your Username or Email and password.',
                'login_id': login_id,
                'success': success,
            })

        # Find user by username or email
        user_obj = None
        if User.objects.filter(username__iexact=login_id).exists():
            user_obj = User.objects.get(username__iexact=login_id)
        elif User.objects.filter(email__iexact=login_id).exclude(email='').exists():
            user_obj = User.objects.filter(email__iexact=login_id).exclude(email='').first()

        if user_obj and not user_obj.is_active:
            return render(request, 'signin.html', {
                'error': 'Your account has been locked due to multiple failed attempts. Please contact the administrator.',
                'is_locked': True,
                'login_id': login_id,
                'success': success,
            })

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
            is_locked = False
            if user_obj:
                user_obj.refresh_from_db()
                if not user_obj.is_active:
                    error_msg = 'Your account has been locked due to 5 failed login attempts. Please contact the administrator.'
                    is_locked = True
                else:
                    error_msg = 'Invalid Username/Email address or password.'
            else:
                error_msg = 'Invalid Username/Email address or password.'

            return render(request, 'signin.html', {
                'error': error_msg,
                'is_locked': is_locked,
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
    is_locked = False
    step = 1
    form_data = {}

    if request.method == 'POST':
        action_step = request.POST.get('step', '1')

        if action_step == '1':
            login_id = request.POST.get('loginId', request.POST.get('username', request.POST.get('login_id', ''))).strip()
            security_question = request.POST.get('securityQuestion', '').strip()
            security_answer = request.POST.get('securityAnswer', '').strip()

            form_data = {
                'loginId': login_id,
                'securityQuestion': security_question,
                'securityAnswer': security_answer,
            }

            if not login_id:
                error = "Please enter your Username or Email."
            elif not security_question:
                error = "Please select your security question."
            elif not security_answer:
                error = "Security answer is required."
            else:
                profile = None
                if User.objects.filter(username__iexact=login_id).exists():
                    user_obj = User.objects.get(username__iexact=login_id)
                    profile = getattr(user_obj, 'student_profile', None)
                elif User.objects.filter(email__iexact=login_id).exclude(email='').exists():
                    user_obj = User.objects.filter(email__iexact=login_id).exclude(email='').first()
                    profile = getattr(user_obj, 'student_profile', None)
                elif StudentProfile.objects.filter(username__iexact=login_id).exists():
                    profile = StudentProfile.objects.filter(username__iexact=login_id).first()

                if profile:
                    if profile.user and not profile.user.is_active:
                        error = "Your account has been locked due to multiple failed attempts. Please contact the administrator."
                        is_locked = True
                    elif (profile.security_question == security_question and
                        profile.security_answer and
                        profile.security_answer.strip().lower() == security_answer.strip().lower()):
                        # Verification successful! Advance to Step 2.
                        request.session['reset_user_id'] = profile.user.id
                        request.session['reset_username'] = profile.username or profile.user.username
                        step = 2
                    else:
                        ActivityLog.objects.create(
                            user=profile.user,
                            action='FAILED_PASSWORD_RESET',
                            details=f"Failed password reset verification for user '{login_id}' (security answer or question mismatch)."
                        )
                        locked = check_and_lock_account(profile.user, 'FAILED_PASSWORD_RESET')
                        if locked or (profile.user and not profile.user.is_active):
                            error = "Your account has been locked due to 5 failed security question attempts. Please contact the administrator."
                            is_locked = True
                        else:
                            error = "The security question or answer does not match our records."
                else:
                    error = "No student account found with the provided Username or Email."
                    ActivityLog.objects.create(
                        user=None,
                        action='FAILED_PASSWORD_RESET',
                        details=f"Failed password reset attempt for non-existent user: '{login_id}'."
                    )

        elif action_step == '2':
            reset_user_id = request.session.get('reset_user_id')
            if not reset_user_id:
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
                        user = User.objects.get(id=reset_user_id)
                        user.set_password(password)
                        user.save()

                        if 'reset_user_id' in request.session:
                            del request.session['reset_user_id']
                        if 'reset_username' in request.session:
                            del request.session['reset_username']

                        return redirect('/signin/?reset=success')
                    except User.DoesNotExist:
                        error = "User account not found. Please try again."
                        step = 1

    return render(request, 'forgot_password.html', {
        'error': error,
        'is_locked': is_locked,
        'step': step,
        'form_data': form_data,
        'username': request.session.get('reset_username', '') if step == 2 else ''
    })



def signout(request):
    logout(request)
    return redirect('signin')


@login_required(login_url='signin')
def dashboard(request):
    student_name = "Student"
    has_taken_assessment = False
    assessment_result = None

    if request.user.is_authenticated:
        profile = getattr(request.user, 'student_profile', None)
        if profile:
            if profile.full_name:
                student_name = profile.full_name
            elif request.user.first_name:
                student_name = request.user.first_name
            elif request.user.username:
                student_name = request.user.username

            assessment_result = getattr(profile, 'assessment_result', None)
            if assessment_result:
                has_taken_assessment = True
            elif StudentAptitudeResponse.objects.filter(student=profile).exists() or StudentInterestResponse.objects.filter(student=profile).exists():
                has_taken_assessment = True

    if student_name:
        student_name = student_name.title()

    return render(request, 'assessment/dashboard.html', {
        'student_name': student_name,
        'has_taken_assessment': has_taken_assessment,
        'assessment_result': assessment_result,
    })


@login_required(login_url='signin')
def retake_assessment(request):
    student_profile = getattr(request.user, 'student_profile', None)
    if student_profile:
        # Reset existing responses and calculated result for a fresh start
        StudentAptitudeResponse.objects.filter(student=student_profile).delete()
        StudentInterestResponse.objects.filter(student=student_profile).delete()
        AssessmentResult.objects.filter(student=student_profile).delete()
        
        # Reset session randomized question order caches so next attempt gets fresh permutations
        request.session.pop('aptitude_shuffled_ids', None)
        request.session.pop('preference_shuffled_ids', None)

        ActivityLog.objects.create(
            user=request.user,
            action='ASSESSMENT_RETAKEN',
            details=f"Student '{student_profile.full_name or request.user.username}' reset their assessment for a fresh retake."
        )
    return redirect('aptitude_ready')


@login_required(login_url='signin')
def aptitude_ready(request):
    return render(request, 'assessment/aptitude-ready.html')



@login_required(login_url='signin')
def assess_aptitude(request):
    student_profile = request.user.student_profile
    active_questions = list(AptitudeQuestion.objects.filter(status=True))

    # Maintain stable randomized question order in session for this assessment attempt
    shuffled_ids = request.session.get('aptitude_shuffled_ids')
    active_ids = {q.question_id for q in active_questions}

    if not shuffled_ids or set(shuffled_ids) != active_ids:
        ids_list = [q.question_id for q in active_questions]
        random.shuffle(ids_list)
        shuffled_ids = ids_list
        request.session['aptitude_shuffled_ids'] = shuffled_ids

    # Order questions according to shuffled_ids
    questions_map = {q.question_id: q for q in active_questions}
    questions = [questions_map[qid] for qid in shuffled_ids if qid in questions_map]

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
        ActivityLog.objects.create(
            user=request.user,
            action='ASSESSMENT_COMPLETED',
            details=f"Student '{student_profile.full_name or request.user.username}' completed the Aptitude Assessment."
        )
        return redirect('preference_ready')

    existing_responses = StudentAptitudeResponse.objects.filter(student=student_profile)
    user_answers = {resp.question_id: resp.selected_answer for resp in existing_responses}

    import json
    return render(request, 'assessment/aptitude-assess.html', {
        'questions': questions,
        'user_answers': user_answers,
        'user_answers_json': json.dumps(user_answers),
        'total_questions': len(questions),
    })


@login_required(login_url='signin')
def preference_ready(request):
    return render(request, 'assessment/preference-ready.html')


@login_required(login_url='signin')
def assess_preference(request):
    student_profile = request.user.student_profile
    all_questions = list(sync_interest_questions())

    # Maintain stable randomized question order in session for this assessment attempt
    shuffled_ids = request.session.get('preference_shuffled_ids')
    active_ids = {q.question_id for q in all_questions}

    if not shuffled_ids or set(shuffled_ids) != active_ids:
        ids_list = [q.question_id for q in all_questions]
        random.shuffle(ids_list)
        shuffled_ids = ids_list
        request.session['preference_shuffled_ids'] = shuffled_ids

    # Order questions according to shuffled_ids
    questions_map = {q.question_id: q for q in all_questions}
    questions = [questions_map[qid] for qid in shuffled_ids if qid in questions_map]

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
        ActivityLog.objects.create(
            user=request.user,
            action='ASSESSMENT_COMPLETED',
            details=f"Student '{student_profile.full_name or request.user.username}' completed the Interest Preference Assessment."
        )
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
def process_results(request):
    """
    AJAX endpoint called during loading page to calculate RIASEC scores via O*NET,
    individual aptitude dimension scores, and program recommendations.
    """
    student_profile = getattr(request.user, 'student_profile', None)
    if not student_profile:
        return JsonResponse({'status': 'error', 'message': 'Student profile not found'}, status=400)

    try:
        result_obj = calculate_and_save_assessment_results(student_profile)
        return JsonResponse({
            'status': 'success',
            'result_id': result_obj.result_id,
            'riasec_code': result_obj.riasec_code,
            'alignment_level': result_obj.alignment_level,
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=500)


@login_required(login_url='signin')
def result(request):
    student_profile = getattr(request.user, 'student_profile', None)
    if not student_profile:
        return redirect('dashboard')

    assessment_result = getattr(student_profile, 'assessment_result', None)
    if not assessment_result:
        assessment_result = calculate_and_save_assessment_results(student_profile)

    # Aptitude Scores Breakdown
    aptitude_items = [
        {
            'name': 'Verbal Reasoning',
            'score': assessment_result.verbal_score,
            'label': lookup_score_interpretation(assessment_result.verbal_score),
            'icon': 'fa-regular fa-comment-dots',
        },
        {
            'name': 'Numerical Reasoning',
            'score': assessment_result.numerical_score,
            'label': lookup_score_interpretation(assessment_result.numerical_score),
            'icon': 'fa-solid fa-calculator',
        },
        {
            'name': 'Logical Reasoning',
            'score': assessment_result.logical_score,
            'label': lookup_score_interpretation(assessment_result.logical_score),
            'icon': 'fa-solid fa-brain',
        },
        {
            'name': 'Spatial Ability',
            'score': assessment_result.spatial_score,
            'label': lookup_score_interpretation(assessment_result.spatial_score),
            'icon': 'fa-solid fa-drafting-compass',
        },
        {
            'name': 'Technical/Mechanical Reasoning',
            'score': assessment_result.technical_score,
            'label': lookup_score_interpretation(assessment_result.technical_score),
            'icon': 'fa-solid fa-gear',
        },
        {
            'name': 'Problem-Solving',
            'score': assessment_result.problem_solving_score,
            'label': lookup_score_interpretation(assessment_result.problem_solving_score),
            'icon': 'fa-solid fa-lightbulb',
        },
    ]

    # RIASEC Area Scores Breakdown (Raw scores 0-40 -> Normalized %)
    r_pct = min(100, round((assessment_result.r_score / 40.0) * 100))
    i_pct = min(100, round((assessment_result.i_score / 40.0) * 100))
    a_pct = min(100, round((assessment_result.a_score / 40.0) * 100))
    s_pct = min(100, round((assessment_result.s_score / 40.0) * 100))
    e_pct = min(100, round((assessment_result.e_score / 40.0) * 100))
    c_pct = min(100, round((assessment_result.c_score / 40.0) * 100))

    riasec_items = [
        {
            'code_letter': 'R',
            'title': 'Realistic',
            'raw_score': assessment_result.r_score,
            'percentage': r_pct,
            'level': lookup_score_interpretation(r_pct),
        },
        {
            'code_letter': 'I',
            'title': 'Investigative',
            'raw_score': assessment_result.i_score,
            'percentage': i_pct,
            'level': lookup_score_interpretation(i_pct),
        },
        {
            'code_letter': 'A',
            'title': 'Artistic',
            'raw_score': assessment_result.a_score,
            'percentage': a_pct,
            'level': lookup_score_interpretation(a_pct),
        },
        {
            'code_letter': 'S',
            'title': 'Social',
            'raw_score': assessment_result.s_score,
            'percentage': s_pct,
            'level': lookup_score_interpretation(s_pct),
        },
        {
            'code_letter': 'E',
            'title': 'Enterprising',
            'raw_score': assessment_result.e_score,
            'percentage': e_pct,
            'level': lookup_score_interpretation(e_pct),
        },
        {
            'code_letter': 'C',
            'title': 'Conventional',
            'raw_score': assessment_result.c_score,
            'percentage': c_pct,
            'level': lookup_score_interpretation(c_pct),
        },
    ]

    # Curated Descriptions for Cognitive Aptitudes
    APTITUDE_DESCRIPTIONS = {
        'Verbal Reasoning': 'Demonstrates strong capability in understanding written ideas, analyzing language, and communicating complex concepts effectively.',
        'Numerical Reasoning': 'Demonstrates proficiency in quantitative analysis, mathematical reasoning, interpreting statistical data, and working with numbers.',
        'Logical Reasoning': 'Demonstrates strong analytical thinking, recognizing logical patterns, evaluating arguments, and drawing sound conclusions.',
        'Spatial Ability': 'Demonstrates high capacity for visualizing 3D objects, understanding spatial relationships, and conceptualizing structural layouts.',
        'Technical/Mechanical Reasoning': 'Demonstrates strong understanding of mechanical principles, physical forces, machinery operations, and practical tools.',
        'Problem-Solving': 'Demonstrates high ability to diagnose complex challenges, break down multifaceted issues, and execute effective solutions.',
    }

    # Curated O*NET Descriptions for RIASEC Themes
    RIASEC_DESCRIPTIONS = {
        'R': {
            'title': 'Realistic (Doers)',
            'description': 'Prefers practical, hands-on activities, working with tools, machinery, materials, or physical tasks in tangible environments.'
        },
        'I': {
            'title': 'Investigative (Thinkers)',
            'description': 'Prefers analytical, scientific, and research-oriented tasks involving problem-solving, data analysis, and intellectual inquiry.'
        },
        'A': {
            'title': 'Artistic (Creators)',
            'description': 'Prefers creative self-expression, original design, visual or literary arts, and innovative projects without rigid rules.'
        },
        'S': {
            'title': 'Social (Helpers)',
            'description': 'Prefers assisting, teaching, mentoring, and empowering others in collaborative, people-focused environments.'
        },
        'E': {
            'title': 'Enterprising (Persuaders)',
            'description': 'Prefers leading teams, managing projects, persuading others, taking strategic business initiative, and achieving goals.'
        },
        'C': {
            'title': 'Conventional (Organizers)',
            'description': 'Prefers structured workflows, systematic data management, attention to detail, accuracy, and organized record-keeping.'
        },
    }

    # Sort and extract Top 3 Aptitudes
    top_aptitudes = sorted(aptitude_items, key=lambda x: x['score'], reverse=True)[:3]
    for item in top_aptitudes:
        item['description'] = APTITUDE_DESCRIPTIONS.get(item['name'], '')

    # Sort and extract Top 3 RIASEC Interest Themes
    top_riasec = sorted(riasec_items, key=lambda x: x['percentage'], reverse=True)[:3]
    for item in top_riasec:
        info = RIASEC_DESCRIPTIONS.get(item['code_letter'], {})
        item['full_title'] = info.get('title', item['title'])
        item['description'] = info.get('description', '')

    # Calculate dynamic SVG Radar polygon and dot points
    r_pt = (150, round(120 - 90 * (r_pct / 100.0), 1))
    i_pt = (round(150 + 77.94 * (i_pct / 100.0), 1), round(120 - 45 * (i_pct / 100.0), 1))
    a_pt = (round(150 + 77.94 * (a_pct / 100.0), 1), round(120 + 45 * (a_pct / 100.0), 1))
    s_pt = (150, round(120 + 90 * (s_pct / 100.0), 1))
    e_pt = (round(150 - 77.94 * (e_pct / 100.0), 1), round(120 + 45 * (e_pct / 100.0), 1))
    c_pt = (round(150 - 77.94 * (c_pct / 100.0), 1), round(120 - 45 * (c_pct / 100.0), 1))

    radar_polygon = f"{r_pt[0]},{r_pt[1]} {i_pt[0]},{i_pt[1]} {a_pt[0]},{a_pt[1]} {s_pt[0]},{s_pt[1]} {e_pt[0]},{e_pt[1]} {c_pt[0]},{c_pt[1]}"
    radar_dots = [r_pt, i_pt, a_pt, s_pt, e_pt, c_pt]

    # Calculate detailed recommendations with individual scores and alignment levels
    prog_recs = calculate_program_recommendations(
        student_profile=student_profile,
        aptitude_scores={
            'numerical_score': assessment_result.numerical_score,
            'logical_score': assessment_result.logical_score,
            'problem_solving_score': assessment_result.problem_solving_score,
            'spatial_score': assessment_result.spatial_score,
            'technical_score': assessment_result.technical_score,
            'verbal_score': assessment_result.verbal_score,
        },
        riasec_scores={
            'r_score': assessment_result.r_score,
            'i_score': assessment_result.i_score,
            'a_score': assessment_result.a_score,
            's_score': assessment_result.s_score,
            'e_score': assessment_result.e_score,
            'c_score': assessment_result.c_score,
            'riasec_code': assessment_result.riasec_code,
        },
    )
    ranked_programs = prog_recs.get('ranked_programs', [])
    top_program = ranked_programs[0] if len(ranked_programs) > 0 else None
    second_program = ranked_programs[1] if len(ranked_programs) > 1 else None
    third_program = ranked_programs[2] if len(ranked_programs) > 2 else None

    # Check if programs have majors
    top_has_majors = bool(top_program and top_program['has_majors'])
    second_has_majors = bool(second_program and second_program['has_majors'])
    third_has_majors = bool(third_program and third_program['has_majors'])

    return render(request, 'assessment/result.html', {
        'result': assessment_result,
        'top_program': top_program,
        'second_program': second_program,
        'third_program': third_program,
        'ranked_programs': ranked_programs,
        'aptitude_items': aptitude_items,
        'riasec_items': riasec_items,
        'top_aptitudes': top_aptitudes,
        'top_riasec': top_riasec,
        'radar_polygon': radar_polygon,
        'radar_dots': radar_dots,
        'top_has_majors': top_has_majors,
        'second_has_majors': second_has_majors,
        'third_has_majors': third_has_majors,
    })


@login_required(login_url='signin')
def major_recommendations(request, program_id):
    """
    Detailed Major Recommendation analysis page for a specific degree program.
    Evaluates student's cognitive aptitude and RIASEC interest alignment against
    the program's specialized majors.
    """
    student_profile = getattr(request.user, 'student_profile', None)
    if not student_profile:
        return redirect('dashboard')

    assessment_result = getattr(student_profile, 'assessment_result', None)
    if not assessment_result:
        assessment_result = calculate_and_save_assessment_results(student_profile)

    program = get_object_or_404(Program, pk=program_id)

    # Ensure program has majors
    if not program.majors.exists():
        return redirect('result')

    aptitude_scores = {
        'numerical_score': assessment_result.numerical_score,
        'logical_score': assessment_result.logical_score,
        'problem_solving_score': assessment_result.problem_solving_score,
        'spatial_score': assessment_result.spatial_score,
        'technical_score': assessment_result.technical_score,
        'verbal_score': assessment_result.verbal_score,
    }
    riasec_scores = {
        'r_score': assessment_result.r_score,
        'i_score': assessment_result.i_score,
        'a_score': assessment_result.a_score,
        's_score': assessment_result.s_score,
        'e_score': assessment_result.e_score,
        'c_score': assessment_result.c_score,
        'riasec_code': assessment_result.riasec_code,
    }

    major_analysis = calculate_major_recommendations(
        student_profile=student_profile,
        program=program,
        aptitude_scores=aptitude_scores,
        riasec_scores=riasec_scores,
    )

    return render(request, 'assessment/major_result.html', {
        'program': program,
        'result': assessment_result,
        'top_majors': major_analysis['top_majors'],
        'all_majors': major_analysis['all_majors'],
    })






