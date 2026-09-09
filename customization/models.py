from django.db import models
from django.db.models.signals import post_save

DEFAULT_DIMENSIONS = [
    'Numerical Reasoning',
    'Logical Reasoning',
    'Problem-Solving',
    'Spatial Ability',
    'Technical/Mechanical Reasoning',
    'Verbal/Communication Ability',
    'Realistic',
    'Investigative',
    'Artistic',
    'Social',
    'Enterprising',
    'Conventional',
]


class Program(models.Model):
    """
    Master list of academic degree programs evaluated by the system.
    """
    program_id = models.AutoField(primary_key=True)
    program_name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=30, unique=True)
    description = models.TextField()
    min_gwa = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        null=True,
        blank=True,
        verbose_name="Minimum GWA Cutoff",
        help_text="Optional minimum GWA required for admission/recommendation (e.g., 85.00). Students with GWA below this value are disqualified."
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.abbreviation} - {self.program_name}"


class AptitudeQuestion(models.Model):
    """
    Test items for the researcher-adapted cognitive and aptitude test.
    """
    DIMENSION_CHOICES = [
        ('Numerical Reasoning', 'Numerical Reasoning'),
        ('Logical Reasoning', 'Logical Reasoning'),
        ('Problem-Solving', 'Problem-Solving'),
        ('Spatial Ability', 'Spatial Ability'),
        ('Technical/Mechanical Reasoning', 'Technical/Mechanical Reasoning'),
        ('Verbal/Communication Ability', 'Verbal/Communication Ability'),
    ]


    ANSWER_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]

    question_id = models.AutoField(primary_key=True)
    dimension = models.CharField(max_length=100, choices=DIMENSION_CHOICES, verbose_name="Dimension")
    question_text = models.TextField(verbose_name="Question Text")
    option_a = models.CharField(max_length=255, verbose_name="Option A")
    option_b = models.CharField(max_length=255, verbose_name="Option B")
    option_c = models.CharField(max_length=255, verbose_name="Option C")
    option_d = models.CharField(max_length=255, verbose_name="Option D")
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES, verbose_name="Correct Answer")
    status = models.BooleanField(default=True, verbose_name="Active?")
    for_validation = models.BooleanField(default=True, verbose_name="For Validation?")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"Q{self.question_id} ({self.dimension}): {self.question_text[:50]}..."

    class Meta:
        verbose_name_plural = "Aptitude Questions"


class InterestQuestion(models.Model):
    """
    60 work-activity items adapted from the O*NET Interest Profiler Short Form.
    """
    RIASEC_CHOICES = [
        ('R', 'Realistic'),
        ('I', 'Investigative'),
        ('A', 'Artistic'),
        ('S', 'Social'),
        ('E', 'Enterprising'),
        ('C', 'Conventional'),
    ]

    question_id = models.AutoField(primary_key=True)
    item_number = models.PositiveIntegerField(unique=True, verbose_name="Item Number")
    riasec_area = models.CharField(max_length=1, choices=RIASEC_CHOICES, verbose_name="RIASEC Area")
    question_text = models.TextField(verbose_name="Question Text")
    status = models.BooleanField(default=True, verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created At")

    def __str__(self):
        return f"Item {self.item_number} ({self.riasec_area}): {self.question_text[:50]}..."

    class Meta:
        verbose_name_plural = "Interest Questions"


class ProgramCriteria(models.Model):
    """
    Configurable scoring weights and minimum thresholds per program and dimension.
    """
    MINIMUM_LEVEL_CHOICES = [
        ('Very High', 'Very High'),
        ('High', 'High'),
        ('Moderate', 'Moderate'),
        ('Low', 'Low'),
        ('Very Low', 'Very Low'),
        ('Not Applicable', 'Not Applicable'),
    ]

    criterion_id = models.AutoField(primary_key=True, verbose_name="Criterion ID")
    program = models.ForeignKey(
        'customization.Program',
        on_delete=models.CASCADE,
        related_name='criteria',
        verbose_name="Program"
    )
    dimension_name = models.CharField(max_length=100, verbose_name="Dimension Name")
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Weight")
    minimum_level = models.CharField(
        max_length=20,
        choices=MINIMUM_LEVEL_CHOICES,
        default='Not Applicable',
        verbose_name="Minimum Level"
    )

    def __str__(self):
        return f"{self.program.abbreviation} Criteria - {self.dimension_name} (weight={self.weight})"

    class Meta:
        verbose_name_plural = "Program Criteria"


class Major(models.Model):
    """
    Academic specialization / major offered under a degree program.
    """
    major_id = models.AutoField(primary_key=True)
    program = models.ForeignKey(
        'customization.Program',
        on_delete=models.CASCADE,
        related_name='majors',
        verbose_name="Program"
    )
    name = models.CharField(max_length=255, verbose_name="Major Name")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.program.abbreviation} - {self.name}"

    class Meta:
        verbose_name = "Major"
        verbose_name_plural = "Majors"
        ordering = ['program', 'name']


class MajorCriteria(models.Model):
    """
    Configurable scoring weights and minimum thresholds per major and dimension.
    """
    MINIMUM_LEVEL_CHOICES = [
        ('Very High', 'Very High'),
        ('High', 'High'),
        ('Moderate', 'Moderate'),
        ('Low', 'Low'),
        ('Very Low', 'Very Low'),
        ('Not Applicable', 'Not Applicable'),
    ]

    criterion_id = models.AutoField(primary_key=True, verbose_name="Criterion ID")
    major = models.ForeignKey(
        'customization.Major',
        on_delete=models.CASCADE,
        related_name='criteria',
        verbose_name="Major"
    )
    dimension_name = models.CharField(max_length=100, verbose_name="Dimension Name")
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Weight")
    minimum_level = models.CharField(
        max_length=20,
        choices=MINIMUM_LEVEL_CHOICES,
        default='Not Applicable',
        verbose_name="Minimum Level"
    )

    def __str__(self):
        return f"{self.major.name} Criteria - {self.dimension_name} (weight={self.weight})"

    class Meta:
        verbose_name = "Major Criterion"
        verbose_name_plural = "Major Criteria"






DEFAULT_SCORE_TIERS = [
    ('Very High', 80.00, 100.00),
    ('High', 60.00, 79.99),
    ('Moderate', 40.00, 59.99),
    ('Low', 20.00, 39.99),
    ('Very Low', 0.00, 19.99),
]


class ScoreInterpretation(models.Model):
    """
    Configurable score ranges and qualitative performance tier bands.
    """
    TIER_CHOICES = [(tier[0], tier[0]) for tier in DEFAULT_SCORE_TIERS]

    id = models.AutoField(primary_key=True, verbose_name="ID")
    label = models.CharField(max_length=50, unique=True, choices=TIER_CHOICES, verbose_name="Label")
    min_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Minimum Score")
    max_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Maximum Score")

    def __str__(self):
        return f"{self.label} ({self.min_score} - {self.max_score})"

    class Meta:
        verbose_name = "Score Interpretation Config"
        verbose_name_plural = "Score Interpretation Config"



from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.contrib.auth.signals import user_logged_in, user_logged_out, user_login_failed


class ActivityLog(models.Model):
    """
    Audit log for recording system activities (logins, logouts, failed attempts, account locking, assessment completions).
    Only visible in the admin panel as read-only.
    """
    ACTION_CHOICES = [
        ('LOGIN', 'User Logged In'),
        ('LOGOUT', 'User Logged Out'),
        ('FAILED_LOGIN', 'Failed Login Attempt'),
        ('FAILED_PASSWORD_RESET', 'Failed Password Reset'),
        ('ACCOUNT_LOCKED', 'Account Locked'),
        ('ASSESSMENT_COMPLETED', 'Assessment Completed'),
        ('ASSESSMENT_RETAKEN', 'Assessment Retaken / Reset'),
    ]

    log_id = models.AutoField(primary_key=True, verbose_name="Log ID")
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='activity_logs',
        verbose_name="User"
    )
    action = models.CharField(max_length=64, choices=ACTION_CHOICES, verbose_name="Action")
    details = models.TextField(blank=True, null=True, verbose_name="Details")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Timestamp")

    def __str__(self):
        user_str = self.user.username if self.user else "System/Unknown"
        return f"[{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')}] {user_str} - {self.get_action_display()}"

    class Meta:
        verbose_name = "Activity Log"
        verbose_name_plural = "Activity Logs"
        ordering = ['-timestamp']


def check_and_lock_account(user, failed_action_type=None):
    """
    Checks recent ActivityLogs for `user`. If 5 consecutive failed attempts
    (FAILED_LOGIN or FAILED_PASSWORD_RESET) occurred without an intervening LOGIN,
    locks the user account (is_active = False) and records an ACCOUNT_LOCKED ActivityLog entry.
    """
    if not user or not user.is_active:
        return False

    recent_logs = ActivityLog.objects.filter(user=user).order_by('-timestamp')[:10]

    failed_count = 0
    for log in recent_logs:
        if log.action in ('FAILED_LOGIN', 'FAILED_PASSWORD_RESET'):
            failed_count += 1
        elif log.action in ('LOGIN', 'ACCOUNT_LOCKED'):
            break

    if failed_count >= 5:
        user.is_active = False
        user.save()

        reason = (
            "failed login attempts" if failed_action_type == 'FAILED_LOGIN'
            else "failed password reset attempts" if failed_action_type == 'FAILED_PASSWORD_RESET'
            else "failed authentication attempts"
        )

        ActivityLog.objects.create(
            user=user,
            action='ACCOUNT_LOCKED',
            details=f"Account for user '{user.username}' was automatically locked due to 5 consecutive {reason}."
        )
        return True
    return False


@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    if user:
        ActivityLog.objects.create(
            user=user,
            action='LOGIN',
            details=f"User '{user.username}' logged into the system."
        )


@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    if user and hasattr(user, 'username'):
        ActivityLog.objects.create(
            user=user,
            action='LOGOUT',
            details=f"User '{user.username}' logged out of the system."
        )


@receiver(user_login_failed)
def log_user_login_failed(sender, credentials, request, **kwargs):
    login_id = credentials.get('username') or credentials.get('email') or 'Unknown'
    user_obj = None
    if User.objects.filter(username__iexact=login_id).exists():
        user_obj = User.objects.get(username__iexact=login_id)
    elif User.objects.filter(email__iexact=login_id).exclude(email='').exists():
        user_obj = User.objects.filter(email__iexact=login_id).exclude(email='').first()

    ActivityLog.objects.create(
        user=user_obj,
        action='FAILED_LOGIN',
        details=f"Failed login attempt using Username/Email identifier: '{login_id}'"
    )

    if user_obj:
        check_and_lock_account(user_obj, 'FAILED_LOGIN')


@receiver(post_save, sender=Program)
def create_default_program_criteria(sender, instance, created, **kwargs):
    for dim in DEFAULT_DIMENSIONS:
        ProgramCriteria.objects.get_or_create(
            program=instance,
            dimension_name=dim,
            defaults={
                'weight': 0.00,
                'minimum_level': 'Not Applicable'
            }
        )


@receiver(post_save, sender=Major)
def create_default_major_criteria(sender, instance, created, **kwargs):
    for dim in DEFAULT_DIMENSIONS:
        MajorCriteria.objects.get_or_create(
            major=instance,
            dimension_name=dim,
            defaults={
                'weight': 0.00,
                'minimum_level': 'Not Applicable'
            }
        )



