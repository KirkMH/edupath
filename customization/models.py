from django.db import models

class Program(models.Model):
    """
    Master list of academic degree programs evaluated by the system.
    """
    program_id = models.AutoField(primary_key=True)
    program_name = models.CharField(max_length=255)
    abbreviation = models.CharField(max_length=30, unique=True)
    description = models.TextField()
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
        ('Deductive Reasoning', 'Deductive Reasoning'),
        ('Inductive Reasoning', 'Inductive Reasoning'),
        ('Problem Sensitivity', 'Problem Sensitivity'),
        ('Visualization', 'Visualization'),
        ('Information Ordering', 'Information Ordering'),
        ('Oral Comprehension', 'Oral Comprehension'),
        ('Oral Expression', 'Oral Expression'),
        ('Originality', 'Originality'),
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
    status = models.BooleanField(default=True, verbose_name="Status")
    for_validation = models.BooleanField(default=True, verbose_name="For Validation")
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
    criterion_id = models.AutoField(primary_key=True, verbose_name="Criterion ID")
    program = models.ForeignKey(
        'customization.Program',
        on_delete=models.CASCADE,
        related_name='criteria',
        verbose_name="Program"
    )
    dimension_name = models.CharField(max_length=100, verbose_name="Dimension Name")
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=1.00, verbose_name="Weight")
    minimum_level = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True, verbose_name="Minimum Level")

    def __str__(self):
        return f"{self.program.abbreviation} Criteria - {self.dimension_name} (weight={self.weight})"

    class Meta:
        verbose_name_plural = "Program Criteria"


class Rule(models.Model):
    """
    IF-THEN evaluation rules and user-facing justification templates.
    """
    rule_id = models.AutoField(primary_key=True, verbose_name="Rule ID")
    program = models.ForeignKey(
        'customization.Program',
        on_delete=models.CASCADE,
        related_name='rules',
        verbose_name="Program"
    )
    condition_expression = models.TextField(verbose_name="Condition Expression")
    score_adjustment = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Score Adjustment")
    explanation_template = models.TextField(verbose_name="Explanation Template")
    status = models.BooleanField(default=True, verbose_name="Status")

    def __str__(self):
        return f"Rule {self.rule_id} for {self.program.abbreviation}"


class ScoreInterpretation(models.Model):
    """
    Configurable score ranges and qualitative performance tier bands.
    """
    id = models.AutoField(primary_key=True, verbose_name="ID")
    label = models.CharField(max_length=50, unique=True, verbose_name="Label")
    min_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Minimum Score")
    max_score = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Maximum Score")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    order = models.PositiveSmallIntegerField(default=0, verbose_name="Order")

    def __str__(self):
        return f"{self.label} ({self.min_score} - {self.max_score})"

    class Meta:
        verbose_name_plural = "Score Interpretations"