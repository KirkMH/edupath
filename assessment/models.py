from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class StudentProfile(models.Model):
    """
    Extends the standard Django User model (Profile Pattern) to store
    student demographics and assessment activity timestamps.
    """
    id = models.AutoField(primary_key=True, verbose_name="ID")
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='student_profile',
        verbose_name="User"
    )
    student_id = models.CharField(max_length=64, blank=True, null=True, unique=True, verbose_name="Student ID")
    full_name = models.CharField(max_length=128, blank=True, null=True, verbose_name="Full Name")
    age = models.PositiveIntegerField(blank=True, null=True, verbose_name="Age")
    sex = models.CharField(max_length=20, blank=True, null=True, verbose_name="Sex")
    security_question = models.CharField(max_length=255, blank=True, null=True, verbose_name="Security Question")
    security_answer = models.CharField(max_length=255, blank=True, null=True, verbose_name="Security Answer")
    last_date_taken = models.DateTimeField(blank=True, null=True, verbose_name="Last Date Taken")

    def __str__(self):
        return f"Profile: {self.user.username} (ID: {self.student_id or 'None'})"

    class Meta:
        verbose_name_plural = "Student Profiles"
        unique_together = ('full_name', 'student_id')



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

    response_id = models.AutoField(primary_key=True, verbose_name="Response ID")
    student = models.ForeignKey(
        'StudentProfile',
        on_delete=models.CASCADE,
        related_name='aptitude_responses',
        verbose_name="Student"
    )
    question = models.ForeignKey(
        'customization.AptitudeQuestion',
        on_delete=models.CASCADE,
        verbose_name="Question"
    )
    selected_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES, verbose_name="Selected Answer")
    is_correct = models.BooleanField(verbose_name="Correct?")

    def __str__(self):
        return f"{self.student.user.username} - Aptitude Q{self.question_id} ({'Correct' if self.is_correct else 'Incorrect'})"

    class Meta:
        verbose_name_plural = "Student Aptitude Responses"


class StudentInterestResponse(models.Model):
    """
    Records the student's latest submitted 5-point Likert rating for each
    O*NET RIASEC interest item.
    """
    response_id = models.AutoField(primary_key=True, verbose_name="Response ID")
    student = models.ForeignKey(
        'StudentProfile',
        on_delete=models.CASCADE,
        related_name='interest_responses',
        verbose_name="Student"
    )
    question = models.ForeignKey(
        'customization.InterestQuestion',
        on_delete=models.CASCADE,
        verbose_name="Question"
    )
    # Scale: 1 (Strongly Dislike) to 5 (Strongly Like)
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Rating"
    )

    def __str__(self):
        return f"{self.student.user.username} - Interest Q{self.question_id} (Rating: {self.rating})"

    class Meta:
        verbose_name_plural = "Student Interest Responses"


class AssessmentResult(models.Model):
    """
    Maintains the latest calculated aptitude dimension scores, RIASEC profile,
    and top 3 recommended academic programs per student.
    """
    result_id = models.AutoField(primary_key=True, verbose_name="Result ID")
    student = models.OneToOneField(
        'StudentProfile',
        on_delete=models.CASCADE,
        related_name='assessment_result',
        verbose_name="Student"
    )
    # Serialized map of dimension -> normalized score
    aptitude_scores_json = models.JSONField(verbose_name="Aptitude Scores")
    r_score = models.PositiveIntegerField(verbose_name="R Score")
    i_score = models.PositiveIntegerField(verbose_name="I Score")
    a_score = models.PositiveIntegerField(verbose_name="A Score")
    s_score = models.PositiveIntegerField(verbose_name="S Score")
    e_score = models.PositiveIntegerField(verbose_name="E Score")
    c_score = models.PositiveIntegerField(verbose_name="C Score")
    riasec_code = models.CharField(max_length=10, verbose_name="RIASEC Code")  # e.g., 'R-A-C'
    top_recommended_program = models.ForeignKey(
        'customization.Program',
        on_delete=models.SET_NULL,
        null=True,
        related_name='first_recommendations',
        verbose_name="Top Recommended Program"
    )
    second_recommended_program = models.ForeignKey(
        'customization.Program',
        on_delete=models.SET_NULL,
        null=True,
        related_name='second_recommendations',
        verbose_name="Second Recommended Program"
    )
    third_recommended_program = models.ForeignKey(
        'customization.Program',
        on_delete=models.SET_NULL,
        null=True,
        related_name='third_recommendations',
        verbose_name="Third Recommended Program"
    )
    alignment_level = models.CharField(max_length=50, verbose_name="Alignment Level")  # e.g., 'High', 'Moderate'
    generated_explanation = models.TextField(verbose_name="Generated Explanation")
    date_generated = models.DateTimeField(auto_now=True, verbose_name="Date Generated")

    def __str__(self):
        return f"Result: {self.student.user.username} (RIASEC: {self.riasec_code})"

    class Meta:
        verbose_name_plural = "Assessment Results"