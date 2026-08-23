from django.contrib import admin
from django.db.models import Case, When, Value, IntegerField
from .models import Program, AptitudeQuestion, ProgramCriteria, ScoreInterpretation, InterestQuestion, ActivityLog, DEFAULT_DIMENSIONS, DEFAULT_SCORE_TIERS




from django.contrib.auth.models import Group, User
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

# Configure Admin site header and titles
admin.site.site_header = "EduPath Administration"
admin.site.site_title = "EduPath Administration"
admin.site.index_title = "Welcome to EduPath Portal"

# Unregister Group model
try:
    admin.site.unregister(Group)
except admin.sites.NotRegistered:
    pass

# Unregister default User admin and register CustomUserAdmin
try:
    admin.site.unregister(User)
except admin.sites.NotRegistered:
    pass


@admin.register(User)
class CustomUserAdmin(BaseUserAdmin):
    """
    Customized UserAdmin that removes Groups, user Permissions, and staff status (is_staff)
    from the Users maintenance form in the Django admin panel.
    """
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Permissions', {'fields': ('is_active', 'is_superuser')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    filter_horizontal = ()
    filter_vertical = ()
    list_filter = ('is_superuser', 'is_active')
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_active', 'is_superuser')


class ProgramCriteriaInline(admin.TabularInline):
    model = ProgramCriteria
    extra = 0
    max_num = 0
    can_delete = False
    fields = ('dimension_name', 'weight', 'minimum_level')
    readonly_fields = ('dimension_name',)

    def has_add_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        whens = [When(dimension_name=dim, then=Value(i)) for i, dim in enumerate(DEFAULT_DIMENSIONS)]
        return qs.annotate(
            custom_order=Case(*whens, default=Value(99), output_field=IntegerField())
        ).order_by('custom_order')


@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('abbreviation', 'program_name', 'created_at')
    search_fields = ('program_name', 'abbreviation')
    inlines = [ProgramCriteriaInline]

    def get_formsets_with_inlines(self, request, obj=None):
        if obj:
            for dim in DEFAULT_DIMENSIONS:
                ProgramCriteria.objects.get_or_create(
                    program=obj,
                    dimension_name=dim,
                    defaults={
                        'weight': 0.00,
                        'minimum_level': 'Not Applicable'
                    }
                )
        return super().get_formsets_with_inlines(request, obj)



@admin.register(AptitudeQuestion)
class AptitudeQuestionAdmin(admin.ModelAdmin):
    list_display = ('question_id', 'dimension', 'question_text_short', 'correct_answer', 'status', 'for_validation')
    list_filter = ('dimension', 'status', 'for_validation')
    search_fields = ('question_text', 'dimension')

    def question_text_short(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Question Text'





@admin.register(ScoreInterpretation)
class ScoreInterpretationAdmin(admin.ModelAdmin):
    list_display = ('label', 'min_score', 'max_score')
    readonly_fields = ('label',)
    fields = ('label', 'min_score', 'max_score')

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        for label, default_min, default_max in DEFAULT_SCORE_TIERS:
            ScoreInterpretation.objects.get_or_create(
                label=label,
                defaults={'min_score': default_min, 'max_score': default_max}
            )
        return super().changelist_view(request, extra_context=extra_context)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        tiers = [t[0] for t in DEFAULT_SCORE_TIERS]
        whens = [When(label=tier_name, then=Value(i)) for i, tier_name in enumerate(tiers)]
        return qs.filter(label__in=tiers).annotate(
            tier_order=Case(*whens, default=Value(99), output_field=IntegerField())
        ).order_by('tier_order')




@admin.register(InterestQuestion)
class InterestQuestionAdmin(admin.ModelAdmin):
    list_display = ('item_number', 'riasec_area', 'question_text_short', 'status', 'created_at')
    list_filter = ('riasec_area', 'status')
    search_fields = ('question_text', 'item_number')
    ordering = ('item_number',)

    def question_text_short(self, obj):
        return obj.question_text[:50] + "..." if len(obj.question_text) > 50 else obj.question_text
    question_text_short.short_description = 'Question Text'


@admin.register(ActivityLog)
class ActivityLogAdmin(admin.ModelAdmin):
    """
    Read-only Django admin interface for inspecting system activity logs.
    """
    list_display = ('timestamp', 'user', 'action', 'details')
    list_filter = ('action', 'timestamp')
    search_fields = ('user__username', 'user__first_name', 'user__last_name', 'details')
    ordering = ('-timestamp',)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    def get_readonly_fields(self, request, obj=None):
        return [f.name for f in self.model._meta.fields]
