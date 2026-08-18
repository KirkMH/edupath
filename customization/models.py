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
    ANSWER_CHOICES = [
        ('A', 'A'),
        ('B', 'B'),
        ('C', 'C'),
        ('D', 'D'),
    ]

    question_id = models.AutoField(primary_key=True)
    dimension = models.CharField(max_length=100)
    question_text = models.TextField()
    option_a = models.CharField(max_length=255)
    option_b = models.CharField(max_length=255)
    option_c = models.CharField(max_length=255)
    option_d = models.CharField(max_length=255)
    correct_answer = models.CharField(max_length=1, choices=ANSWER_CHOICES)
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Q{self.question_id} ({self.dimension}): {self.question_text[:50]}..."


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
    item_number = models.PositiveIntegerField(unique=True)
    riasec_area = models.CharField(max_length=1, choices=RIASEC_CHOICES)
    question_text = models.TextField()
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Item {self.item_number} ({self.riasec_area}): {self.question_text[:50]}..."


class ProgramCriteria(models.Model):
    """
    Configurable scoring weights and minimum thresholds per program and dimension.
    """
    criterion_id = models.AutoField(primary_key=True)
    program = models.ForeignKey(
        'customization.Program',
        on_delete=models.CASCADE,
        related_name='criteria'
    )
    dimension_name = models.CharField(max_length=100)
    weight = models.DecimalField(max_digits=5, decimal_places=2, default=1.00)
    minimum_level = models.DecimalField(max_digits=5, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f"{self.program.abbreviation} Criteria - {self.dimension_name} (weight={self.weight})"


class Rule(models.Model):
    """
    IF-THEN evaluation rules and user-facing justification templates.
    """
    rule_id = models.AutoField(primary_key=True)
    program = models.ForeignKey(
        'customization.Program',
        on_delete=models.CASCADE,
        related_name='rules'
    )
    condition_expression = models.TextField()
    score_adjustment = models.DecimalField(max_digits=5, decimal_places=2)
    explanation_template = models.TextField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return f"Rule {self.rule_id} for {self.program.abbreviation}"


class ScoreInterpretation(models.Model):
    """
    Configurable score ranges and qualitative performance tier bands.
    """
    id = models.AutoField(primary_key=True)
    label = models.CharField(max_length=50, unique=True)
    min_score = models.DecimalField(max_digits=5, decimal_places=2)
    max_score = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    order = models.PositiveSmallIntegerField(default=0)

    def __str__(self):
        return f"{self.label} ({self.min_score} - {self.max_score})"
