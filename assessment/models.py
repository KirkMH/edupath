from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class StudentProfile(models.Model):
    """
    Extends the standard Django User model (Profile Pattern) to store
    student demographics and assessment activity timestamps.
    """
    id = models.AutoField(primary_key=True)
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile'
    )
    student_id = models.CharField(max_length=64, blank=True, null=True, unique=True)
    full_name = models.CharField(max_length=128, blank=True, null=True)
    age = models.PositiveIntegerField(blank=True, null=True)
    sex = models.CharField(max_length=20, blank=True, null=True)
    last_date_taken = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return f"Profile: {self.user.username} (ID: {self.student_id or 'None'})"


class StudentAptitudeResponse(models.Model):
    """
    Records the student's latest submitted answer for each aptitude test item.
    """
    ANSWER_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]

    response_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        'StudentProfile',
        on_delete=models.CASCADE,
        related_name='aptitude_responses'
    )
    question = models.ForeignKey(
        'customization.AptitudeQuestion',
        on_delete=models.CASCADE
    )
    selected_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)
    is_correct = models.BooleanField()

    def __str__(self):
        return f"{self.student.user.username} - Aptitude Q{self.question_id} ({'Correct' if self.is_correct else 'Incorrect'})"


class StudentInterestResponse(models.Model):
    """
    Records the student's latest submitted 5-point Likert rating for each
    O*NET RIASEC interest item.
    """
    response_id = models.AutoField(primary_key=True)
    student = models.ForeignKey(
        'StudentProfile',
        on_delete=models.CASCADE,
        related_name='interest_responses'
    )
    question = models.ForeignKey(
        'customization.InterestQuestion',
        on_delete=models.CASCADE
    )
    # Scale: 1 (Strongly Dislike) to 5 (Strongly Like)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    def __str__(self):
        return f"{self.student.user.username} - Interest Q{self.question_id} (Rating: {self.rating})"


class AssessmentResult(models.Model):
    """
    Maintains the latest calculated aptitude dimension scores, RIASEC profile,
    and top 3 recommended academic programs per student.
    """
    result_id = models.AutoField(primary_key=True)
    student = models.OneToOneField(
        'StudentProfile',
        on_delete=models.CASCADE,
        related_name='assessment_result'
    )
    # Serialized map of dimension -> normalized score
    aptitude_scores_json = models.JSONField()
    r_score = models.PositiveIntegerField()
    i_score = models.PositiveIntegerField()
    a_score = models.PositiveIntegerField()
    s_score = models.PositiveIntegerField()
    e_score = models.PositiveIntegerField()
    c_score = models.PositiveIntegerField()
    riasec_code = models.CharField(max_length=10)  # e.g., 'R-A-C'
    top_recommended_program = models.ForeignKey(
        'customization.Program',
        on_delete=models.SET_NULL,
        null=True,
        related_name='first_recommendations'
    )
    second_recommended_program = models.ForeignKey(
        'customization.Program',
        on_delete=models.SET_NULL,
        null=True,
        related_name='second_recommendations'
    )
    third_recommended_program = models.ForeignKey(
        'customization.Program',
        on_delete=models.SET_NULL,
        null=True,
        related_name='third_recommendations'
    )
    alignment_level = models.CharField(max_length=50)  # e.g., 'High', 'Moderate'
    generated_explanation = models.TextField()
    date_generated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Result: {self.student.user.username} (RIASEC: {self.riasec_code})"
