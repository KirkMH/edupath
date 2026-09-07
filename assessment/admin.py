from django.contrib import admin
from .models import StudentProfile, StudentAptitudeResponse, StudentInterestResponse, AssessmentResult


@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'full_name', 'user', 'gwa', 'age', 'sex', 'last_date_taken')
    search_fields = ('username', 'full_name', 'user__username', 'user__email')
    list_filter = ('sex', 'age')


@admin.register(StudentAptitudeResponse)
class StudentAptitudeResponseAdmin(admin.ModelAdmin):
    list_display = ('response_id', 'student', 'question', 'selected_answer', 'is_correct')
    list_filter = ('is_correct', 'selected_answer')
    search_fields = ('student__full_name', 'student__username', 'student__user__username')


@admin.register(StudentInterestResponse)
class StudentInterestResponseAdmin(admin.ModelAdmin):
    list_display = ('response_id', 'student', 'question', 'rating')
    list_filter = ('rating',)
    search_fields = ('student__full_name', 'student__username', 'student__user__username')


@admin.register(AssessmentResult)
class AssessmentResultAdmin(admin.ModelAdmin):
    list_display = ('result_id', 'student', 'riasec_code', 'alignment_level', 'top_recommended_program', 'date_generated')
    list_filter = ('alignment_level', 'date_generated')
    search_fields = ('student__full_name', 'student__username', 'student__user__username', 'riasec_code')

