from django.contrib import admin
from .models import Program, AptitudeQuestion, ProgramCriteria, Rule, ScoreInterpretation

from django.contrib.auth.models import Group

# Configure Admin site header and titles
admin.site.site_header = "EduPath Administration"
admin.site.site_title = "EduPath Administration"
admin.site.index_title = "Welcome to EduPath Portal"

# Unregister Group model
try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('abbreviation', 'program_name', 'created_at')
    search_fields = ('program_name', 'abbreviation')


@admin.register(AptitudeQuestion)
class AptitudeQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'dimension', 'question_text_short', 'correct_answer', 'status')
    list_filter = ('dimension', 'status')
    search_fields = ('question_text', 'dimension')

    def question_text_short(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Question Text'


@admin.register(ProgramCriteria)
class ProgramCriteriaAdmin(admin.ModelAdmin):
    list_display = ('program', 'dimension_name', 'weight', 'minimum_level')
    list_filter = ('program', 'dimension_name')
    search_fields = ('dimension_name', 'program__abbreviation', 'program__program_name')


@admin.register(Rule)
class RuleAdmin(admin.ModelAdmin):
    list_display = ('rule_id', 'program', 'condition_expression', 'score_adjustment', 'status')
    list_filter = ('program', 'status')
    search_fields = ('condition_expression', 'program__abbreviation', 'program__program_name')


@admin.register(ScoreInterpretation)
class ScoreInterpretationAdmin(admin.ModelAdmin):
    list_display = ('label', 'min_score', 'max_score', 'order')
    list_filter = ('label',)
    search_fields = ('label', 'description')
    ordering = ('order', 'min_score')


