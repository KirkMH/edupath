from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import StudentProfile


class SignUpAndLoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('signup')
        self.signin_url = reverse('signin')
        self.signout_url = reverse('signout')
        self.dashboard_url = reverse('dashboard')

        # Existing user for login/duplicate testing
        self.existing_user = User.objects.create_user(
            username='student1',
            email='existing@example.com',
            password='Password123!',
            first_name='Existing Student'
        )
        self.existing_profile = StudentProfile.objects.create(
            user=self.existing_user,
            username='student1',
            full_name='Existing Student',
            age=20,
            sex='Male',
            security_question='What was the name of your first pet?',
            security_answer='Fluffy'
        )

    def test_successful_signup_with_email(self):
        data = {
            'fullName': 'Jane Doe',
            'username': 'janedoe',
            'age': '21',
            'sex': 'Female',
            'gwa': '88.50',
            'email': 'jane@example.com',
            'password': 'SecurePassword123!',
            'confirmPassword': 'SecurePassword123!',
            'securityQuestion': 'What was the name of your first pet?',
            'securityAnswer': 'Fluffy',
            'terms': 'on'
        }
        response = self.client.post(self.signup_url, data)
        self.assertRedirects(response, self.dashboard_url)
        self.assertTrue(User.objects.filter(username='janedoe', email='jane@example.com').exists())
        profile = StudentProfile.objects.filter(username='janedoe', full_name='Jane Doe').first()
        self.assertIsNotNone(profile)
        self.assertEqual(float(profile.gwa), 88.50)

    def test_successful_signup_without_email(self):
        data = {
            'fullName': 'No Email Student',
            'username': 'noemailstudent',
            'age': '19',
            'sex': 'Male',
            'gwa': '92.00',
            'email': '',  # Blank email
            'password': 'SecurePassword123!',
            'confirmPassword': 'SecurePassword123!',
            'securityQuestion': 'What was the name of your first pet?',
            'securityAnswer': 'Fluffy',
            'terms': 'on'
        }
        response = self.client.post(self.signup_url, data)
        self.assertRedirects(response, self.dashboard_url)
        profile = StudentProfile.objects.filter(username='noemailstudent', full_name='No Email Student').first()
        self.assertIsNotNone(profile)
        self.assertEqual(float(profile.gwa), 92.00)

    def test_signup_invalid_gwa(self):
        data = {
            'fullName': 'Invalid GWA Student',
            'username': 'invalidgwa',
            'age': '19',
            'sex': 'Male',
            'gwa': '45.00',  # below 50
            'email': '',
            'password': 'SecurePassword123!',
            'confirmPassword': 'SecurePassword123!',
            'securityQuestion': 'What was the name of your first pet?',
            'securityAnswer': 'Fluffy',
            'terms': 'on'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "General Weighted Average (GWA) must be between 50.00 and 100.00.")

        # Non-numeric GWA test
        data['gwa'] = 'abc'
        response2 = self.client.post(self.signup_url, data)
        self.assertEqual(response2.status_code, 200)
        self.assertContains(response2, "Please enter a valid numeric General Weighted Average (GWA).")

    def test_signin_with_username(self):
        data = {
            'login_id': 'student1',
            'password': 'Password123!'
        }
        response = self.client.post(self.signin_url, data)
        self.assertRedirects(response, self.dashboard_url)

    def test_signin_with_email(self):
        data = {
            'login_id': 'existing@example.com',
            'password': 'Password123!'
        }
        response = self.client.post(self.signin_url, data)
        self.assertRedirects(response, self.dashboard_url)

    def test_signin_invalid_password(self):
        data = {
            'login_id': 'student1',
            'password': 'WrongPassword!'
        }
        response = self.client.post(self.signin_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid Username/Email address or password.")

    def test_signout(self):
        self.client.force_login(self.existing_user)
        response = self.client.get(self.signout_url)
        self.assertRedirects(response, self.signin_url)

    def test_admin_logout_redirects_to_signin(self):
        admin_user = User.objects.create_superuser('admin_test', 'admin@example.com', 'AdminPass123!')
        self.client.force_login(admin_user)
        response = self.client.get('/admin/logout/')
        self.assertRedirects(response, self.signin_url)

    def test_unauthenticated_dashboard_redirect(self):
        response = self.client.get(self.dashboard_url)
        self.assertRedirects(response, f"{self.signin_url}?next={self.dashboard_url}")

    def test_password_mismatch(self):
        data = {
            'fullName': 'John Smith',
            'username': 'johnsmith',
            'age': '22',
            'sex': 'Male',
            'gwa': '85.00',
            'email': 'john@example.com',
            'password': 'Password123!',
            'confirmPassword': 'DifferentPassword!',
            'securityQuestion': 'What was the name of your first pet?',
            'securityAnswer': 'Fluffy',
            'terms': 'on'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords do not match.")

    def test_terms_not_ticked(self):
        data = {
            'fullName': 'John Smith',
            'username': 'johnsmith',
            'age': '22',
            'sex': 'Male',
            'gwa': '85.00',
            'email': 'john@example.com',
            'password': 'Password123!',
            'confirmPassword': 'Password123!',
            'securityQuestion': 'What was the name of your first pet?',
            'securityAnswer': 'Fluffy'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You must agree to the Terms &amp; Conditions and Privacy Policy.")

    def test_duplicate_email(self):
        data = {
            'fullName': 'Another Student',
            'username': 'newuser123',
            'age': '20',
            'sex': 'Male',
            'gwa': '85.00',
            'email': 'existing@example.com',
            'password': 'Password123!',
            'confirmPassword': 'Password123!',
            'securityQuestion': 'What was the name of your first pet?',
            'securityAnswer': 'Fluffy',
            'terms': 'on'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "An account with this email address is already registered.")

    def test_duplicate_username(self):
        data = {
            'fullName': 'New Name',
            'username': 'student1',
            'age': '20',
            'sex': 'Female',
            'gwa': '85.00',
            'email': 'newstudent@example.com',
            'password': 'Password123!',
            'confirmPassword': 'Password123!',
            'securityQuestion': 'What was the name of your first pet?',
            'securityAnswer': 'Fluffy',
            'terms': 'on'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This Username is already registered.")

    def test_forgot_password_flow(self):
        forgot_url = reverse('forgot_password')

        # Step 1: Verify Account with Username & Security Answer
        step1_data = {
            'step': '1',
            'loginId': 'student1',
            'securityQuestion': 'What was the name of your first pet?',
            'securityAnswer': 'Fluffy'
        }
        res1 = self.client.post(forgot_url, step1_data)
        self.assertEqual(res1.status_code, 200)
        self.assertContains(res1, "Set a new password for your account")
        self.assertContains(res1, "student1")

        # Step 2: Set New Password
        step2_data = {
            'step': '2',
            'password': 'BrandNewPassword123!',
            'confirmPassword': 'BrandNewPassword123!'
        }
        res2 = self.client.post(forgot_url, step2_data)
        self.assertRedirects(res2, f"{self.signin_url}?reset=success")

        # Verify new password works
        login_res = self.client.post(self.signin_url, {
            'login_id': 'student1',
            'password': 'BrandNewPassword123!'
        })
        self.assertRedirects(login_res, self.dashboard_url)

    def test_dashboard_displays_student_name(self):
        self.client.force_login(self.existing_user)
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Existing Student!")

    def test_admin_login_page_renders(self):
        response = self.client.get('/admin/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Sign in to your account")
        self.assertContains(response, "Sign in to your account")

    def test_aptitude_assessment_flow(self):
        from customization.models import AptitudeQuestion
        from assessment.models import StudentAptitudeResponse

        q1 = AptitudeQuestion.objects.create(
            dimension='Numerical Reasoning',
            question_text='What is 2 + 2?',
            option_a='3', option_b='4', option_c='5', option_d='6',
            correct_answer='B',
            status=True,
            for_validation=True
        )
        q2 = AptitudeQuestion.objects.create(
            dimension='Deductive Reasoning',
            question_text='Inactive question?',
            option_a='A', option_b='B', option_c='C', option_d='D',
            correct_answer='A',
            status=False,
            for_validation=False
        )

        self.client.force_login(self.existing_user)

        # GET request test
        response = self.client.get(reverse('assess_aptitude'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "<b>FOR VALIDATION.</b> What is 2 + 2?")
        self.assertNotContains(response, "Inactive question?")

        # POST submission test
        post_data = {
            f'question_{q1.question_id}': 'B'
        }
        submit_response = self.client.post(reverse('assess_aptitude'), post_data)
        self.assertRedirects(submit_response, reverse('preference_ready'))

        # Verify StudentAptitudeResponse record created
        resp_obj = StudentAptitudeResponse.objects.get(student=self.existing_profile, question=q1)
        self.assertEqual(resp_obj.selected_answer, 'B')
        self.assertTrue(resp_obj.is_correct)


class RiasecAndAssessmentResultTests(TestCase):
    def setUp(self):
        from customization.models import (
            InterestQuestion, AptitudeQuestion, Program, ProgramCriteria, ScoreInterpretation
        )
        from assessment.models import StudentInterestResponse, StudentAptitudeResponse

        self.client = Client()
        self.user = User.objects.create_user(
            username='riasec_tester',
            email='tester@example.com',
            password='TestPassword123!'
        )
        self.profile = StudentProfile.objects.create(
            user=self.user,
            username='riasec_tester',
            full_name='RIASEC Tester',
            age=20,
            sex='Female',
            security_question='What was the name of your first pet?',
            security_answer='Buddy'
        )

        # Create ScoreInterpretation tiers
        ScoreInterpretation.objects.get_or_create(label='Very High', min_score=80.00, max_score=100.00)
        ScoreInterpretation.objects.get_or_create(label='High', min_score=60.00, max_score=79.99)
        ScoreInterpretation.objects.get_or_create(label='Moderate', min_score=40.00, max_score=59.99)
        ScoreInterpretation.objects.get_or_create(label='Low', min_score=20.00, max_score=39.99)
        ScoreInterpretation.objects.get_or_create(label='Very Low', min_score=0.00, max_score=19.99)

        # Create/Sync 60 Interest Questions from O*NET
        from assessment.services import sync_interest_questions
        self.questions = list(sync_interest_questions())
        if not self.questions:
            # Offline test fallback if network unavailable during test run
            dimensions = ['R', 'I', 'A', 'S', 'E', 'C']
            item_counter = 1
            for dim in dimensions:
                for i in range(10):
                    q = InterestQuestion.objects.create(
                        item_number=item_counter,
                        riasec_area=dim,
                        question_text=f"Sample Question {item_counter} for {dim}",
                        status=True
                    )
                    self.questions.append(q)
                    item_counter += 1

        # Create 6 Aptitude Questions (1 per dimension)
        self.apt_questions = []
        apt_dims = [
            'Numerical Reasoning', 'Logical Reasoning', 'Problem-Solving',
            'Spatial Ability', 'Technical/Mechanical Reasoning', 'Verbal/Communication Ability'
        ]
        for dim in apt_dims:
            q = AptitudeQuestion.objects.create(
                dimension=dim,
                question_text=f"Test question for {dim}",
                option_a='A', option_b='B', option_c='C', option_d='D',
                correct_answer='A',
                status=True
            )
            self.apt_questions.append(q)

        # Create Programs and Criteria
        self.prog_eng = Program.objects.create(
            program_name="Bachelor of Science in Computer Engineering",
            abbreviation="BSCpE",
            description="Engineering and computing program."
        )
        # Update BSCpE criteria
        ProgramCriteria.objects.filter(program=self.prog_eng, dimension_name='Realistic').update(weight=30.0, minimum_level='Moderate')
        ProgramCriteria.objects.filter(program=self.prog_eng, dimension_name='Investigative').update(weight=30.0, minimum_level='Moderate')
        ProgramCriteria.objects.filter(program=self.prog_eng, dimension_name='Numerical Reasoning').update(weight=20.0, minimum_level='Moderate')
        ProgramCriteria.objects.filter(program=self.prog_eng, dimension_name='Logical Reasoning').update(weight=20.0, minimum_level='Moderate')

    def test_riasec_scoring_calculation(self):
        """
        Verify that get_riasec_results correctly computes RIASEC scores and top code
        from student interest responses (R=40, I=30, A=20, S=10, E=0, C=0 -> 'R-I-A').
        """
        from assessment.models import StudentInterestResponse
        from assessment.services import get_riasec_results

        # Rating scale: 1=0pts, 2=1pt, 3=2pts, 4=3pts, 5=4pts
        rating_by_dim = {'R': 5, 'I': 4, 'A': 3, 'S': 2, 'E': 1, 'C': 1}
        for q in self.questions:
            rating = rating_by_dim[q.riasec_area]
            StudentInterestResponse.objects.create(
                student=self.profile,
                question=q,
                rating=rating
            )

        results = get_riasec_results(self.profile)

        self.assertEqual(results['r_score'], 40)
        self.assertEqual(results['i_score'], 30)
        self.assertEqual(results['a_score'], 20)
        self.assertEqual(results['s_score'], 10)
        self.assertEqual(results['e_score'], 0)
        self.assertEqual(results['c_score'], 0)
        self.assertEqual(results['riasec_code'], 'R-I-A')

    def test_riasec_offline_fallback_on_api_failure(self):
        """
        Verify that when external O*NET API returns an error or is unreachable,
        get_riasec_results falls back to local database response calculation
        and produces non-zero, accurate scores.
        """
        from assessment.models import StudentInterestResponse
        from assessment.services import get_riasec_results
        from unittest.mock import patch

        rating_by_dim = {'R': 5, 'I': 5, 'A': 4, 'S': 3, 'E': 2, 'C': 1}
        for q in self.questions:
            rating = rating_by_dim[q.riasec_area]
            StudentInterestResponse.objects.create(
                student=self.profile,
                question=q,
                rating=rating
            )

        with patch('assessment.services.OnetWebService.call', return_value={'error': 'HTTP 403 Forbidden'}):
            results = get_riasec_results(self.profile)

        self.assertEqual(results['r_score'], 40)
        self.assertEqual(results['i_score'], 40)
        self.assertEqual(results['a_score'], 30)
        self.assertEqual(results['s_score'], 20)
        self.assertEqual(results['e_score'], 10)
        self.assertEqual(results['c_score'], 0)
        self.assertTrue(results['riasec_code'].startswith('R-I-') or results['riasec_code'].startswith('I-R-'))

    def test_calculate_and_save_assessment_results(self):
        """
        Verify end-to-end master calculation: non-zero RIASEC scores, aptitude scores,
        program recommendations, and non-'Very Low' alignment level are saved to AssessmentResult.
        """
        from assessment.models import StudentInterestResponse, StudentAptitudeResponse, AssessmentResult
        from assessment.services import calculate_and_save_assessment_results

        # Populate interest responses
        for q in self.questions:
            rating = 5 if q.riasec_area in ['R', 'I'] else 3
            StudentInterestResponse.objects.create(
                student=self.profile,
                question=q,
                rating=rating
            )

        # Populate aptitude responses (all correct)
        for q in self.apt_questions:
            StudentAptitudeResponse.objects.create(
                student=self.profile,
                question=q,
                selected_answer='A',
                is_correct=True
            )

        result_obj = calculate_and_save_assessment_results(self.profile)

        self.assertIsNotNone(result_obj)
        self.assertGreater(result_obj.r_score, 0)
        self.assertGreater(result_obj.i_score, 0)
        self.assertEqual(result_obj.numerical_score, 100)
        self.assertEqual(result_obj.logical_score, 100)
        self.assertIn(result_obj.alignment_level, ['High', 'Very High'])
        self.assertNotEqual(result_obj.alignment_level, 'Very Low')
        self.assertEqual(result_obj.top_recommended_program, self.prog_eng)

        # Check DB persistence
        db_result = AssessmentResult.objects.get(student=self.profile)
        self.assertEqual(db_result.result_id, result_obj.result_id)
        self.assertIn('R', db_result.riasec_code)

    def test_assess_preference_submission_and_result_page(self):
        """
        Verify the web assessment flow: POSTing preference responses,
        running process_results AJAX, and rendering the final result page.
        """
        self.client.force_login(self.user)

        # 1. Post preference answers
        post_data = {}
        for q in self.questions:
            post_data[f'q_{q.question_id}'] = '5' if q.riasec_area == 'R' else '4'

        response = self.client.post(reverse('assess_preference'), post_data)
        self.assertRedirects(response, reverse('loading'))

        # 2. Process results AJAX endpoint
        ajax_res = self.client.get(reverse('process_results'))
        self.assertEqual(ajax_res.status_code, 200)
        data = ajax_res.json()
        self.assertEqual(data['status'], 'success')
        self.assertIn('riasec_code', data)
        self.assertNotEqual(data['alignment_level'], 'Very Low')

        # 3. View result page
        result_res = self.client.get(reverse('result'))
        self.assertEqual(result_res.status_code, 200)
        self.assertContains(result_res, "Realistic")
        self.assertContains(result_res, "BSCpE")

    def test_gwa_exact_numeric_cutoff_disqualification(self):
        """
        Verify that a program with min_gwa is strictly disqualified
        when the student's GWA falls below that exact number.
        """
        from assessment.models import StudentInterestResponse, StudentAptitudeResponse
        from assessment.services import calculate_program_recommendations, calculate_aptitude_dimension_scores, get_riasec_results
        from customization.models import Program, ProgramCriteria

        # Student has GWA of 82.00
        self.profile.gwa = 82.00
        self.profile.save()

        # Set BSCpE GWA cutoff to 85.00 directly on Program model
        self.prog_eng.min_gwa = 85.00
        self.prog_eng.save()

        # Create another program without strict GWA cutoff
        prog_it = Program.objects.create(
            program_name="Bachelor of Science in Information Technology",
            abbreviation="BSIT_TEST",
            description="IT program.",
            min_gwa=None
        )
        ProgramCriteria.objects.update_or_create(
            program=prog_it,
            dimension_name='Realistic',
            defaults={'weight': 0.50, 'minimum_level': 'Not Applicable'}
        )

        # Answer all aptitude items correctly and high realistic interest
        for q in self.apt_questions:
            StudentAptitudeResponse.objects.create(student=self.profile, question=q, selected_answer='A', is_correct=True)
        for q in self.questions:
            StudentInterestResponse.objects.create(student=self.profile, question=q, rating=5)

        apt_scores = calculate_aptitude_dimension_scores(self.profile)
        riasec_scores = get_riasec_results(self.profile)
        recs = calculate_program_recommendations(self.profile, apt_scores, riasec_scores)

        # BSCpE should be DISQUALIFIED because 82.00 < 85.00
        self.assertNotEqual(recs['top_recommended_program'], self.prog_eng)
        self.assertNotEqual(recs['second_recommended_program'], self.prog_eng)
        self.assertNotEqual(recs['third_recommended_program'], self.prog_eng)
        self.assertEqual(recs['top_recommended_program'], prog_it)

    def test_gwa_exact_numeric_cutoff_qualification(self):
        """
        Verify that a student meeting/exceeding the min_gwa cutoff is eligible
        and recommended.
        """
        from assessment.models import StudentInterestResponse, StudentAptitudeResponse
        from assessment.services import calculate_program_recommendations, calculate_aptitude_dimension_scores, get_riasec_results

        # Student has GWA of 88.50
        self.profile.gwa = 88.50
        self.profile.save()

        # Set BSCpE GWA cutoff to 85.00 directly on Program model
        self.prog_eng.min_gwa = 85.00
        self.prog_eng.save()

        # Answer all aptitude items correctly and high realistic interest
        for q in self.apt_questions:
            StudentAptitudeResponse.objects.create(student=self.profile, question=q, selected_answer='A', is_correct=True)
        for q in self.questions:
            StudentInterestResponse.objects.create(student=self.profile, question=q, rating=5)

        apt_scores = calculate_aptitude_dimension_scores(self.profile)
        riasec_scores = get_riasec_results(self.profile)
        recs = calculate_program_recommendations(self.profile, apt_scores, riasec_scores)

        # BSCpE should QUALIFY because 88.50 >= 85.00
        self.assertEqual(recs['top_recommended_program'], self.prog_eng)



