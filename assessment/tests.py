from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import StudentProfile


class SignUpAndLoginTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_url = reverse('index')
        self.signin_url = reverse('signin')
        self.signout_url = reverse('signout')
        self.dashboard_url = reverse('dashboard')

        # Existing user for login/duplicate testing
        self.existing_user = User.objects.create_user(
            username='STU-1001',
            email='existing@example.com',
            password='Password123!',
            first_name='Existing Student'
        )
        self.existing_profile = StudentProfile.objects.create(
            user=self.existing_user,
            student_id='STU-1001',
            full_name='Existing Student',
            age=20,
            sex='Male'
        )

    def test_successful_signup_with_email(self):
        data = {
            'fullName': 'Jane Doe',
            'studentId': 'STU-2002',
            'age': '21',
            'sex': 'Female',
            'email': 'jane@example.com',
            'password': 'SecurePassword123!',
            'confirmPassword': 'SecurePassword123!',
            'terms': 'on'
        }
        response = self.client.post(self.signup_url, data)
        self.assertRedirects(response, self.dashboard_url)
        self.assertTrue(User.objects.filter(email='jane@example.com').exists())
        self.assertTrue(StudentProfile.objects.filter(student_id='STU-2002', full_name='Jane Doe').exists())

    def test_successful_signup_without_email(self):
        data = {
            'fullName': 'No Email Student',
            'studentId': 'STU-5005',
            'age': '19',
            'sex': 'Male',
            'email': '',  # Blank email
            'password': 'SecurePassword123!',
            'confirmPassword': 'SecurePassword123!',
            'terms': 'on'
        }
        response = self.client.post(self.signup_url, data)
        self.assertRedirects(response, self.dashboard_url)
        self.assertTrue(StudentProfile.objects.filter(student_id='STU-5005', full_name='No Email Student').exists())

    def test_signin_with_student_id(self):
        data = {
            'login_id': 'STU-1001',
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
            'login_id': 'STU-1001',
            'password': 'WrongPassword!'
        }
        response = self.client.post(self.signin_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Invalid Student ID/Email address or password.")

    def test_signout(self):
        self.client.force_login(self.existing_user)
        response = self.client.get(self.signout_url)
        self.assertRedirects(response, self.signin_url)

    def test_unauthenticated_dashboard_redirect(self):
        response = self.client.get(self.dashboard_url)
        self.assertRedirects(response, f"{self.signin_url}?next={self.dashboard_url}")

    def test_password_mismatch(self):
        data = {
            'fullName': 'John Smith',
            'studentId': 'STU-3003',
            'age': '22',
            'sex': 'Male',
            'email': 'john@example.com',
            'password': 'Password123!',
            'confirmPassword': 'DifferentPassword!',
            'terms': 'on'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Passwords do not match.")

    def test_terms_not_ticked(self):
        data = {
            'fullName': 'John Smith',
            'studentId': 'STU-3003',
            'age': '22',
            'sex': 'Male',
            'email': 'john@example.com',
            'password': 'Password123!',
            'confirmPassword': 'Password123!'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "You must agree to the Terms &amp; Conditions and Privacy Policy.")

    def test_duplicate_email(self):
        data = {
            'fullName': 'Another Student',
            'studentId': 'STU-9999',
            'age': '20',
            'sex': 'Male',
            'email': 'existing@example.com',
            'password': 'Password123!',
            'confirmPassword': 'Password123!',
            'terms': 'on'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "An account with this email address is already registered.")

    def test_duplicate_student_id(self):
        data = {
            'fullName': 'New Name',
            'studentId': 'STU-1001',
            'age': '20',
            'sex': 'Female',
            'email': 'newstudent@example.com',
            'password': 'Password123!',
            'confirmPassword': 'Password123!',
            'terms': 'on'
        }
        response = self.client.post(self.signup_url, data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "This Student ID is already registered.")

    def test_dashboard_displays_student_name(self):
        self.client.force_login(self.existing_user)
        response = self.client.get(self.dashboard_url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Existing Student!")

    def test_admin_login_page_renders(self):
        response = self.client.get('/admin/login/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Administrator's Login")

