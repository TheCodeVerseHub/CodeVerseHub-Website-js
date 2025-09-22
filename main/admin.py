from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Contest, Problem, TestCase, Submission, ContestParticipant, UserProblemStatus, Announcement


class CustomUserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff', 'date_joined')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active', 'date_joined')
    search_fields = ('username', 'first_name', 'last_name', 'email')
    ordering = ('username',)
    
    fieldsets = list(BaseUserAdmin.fieldsets) + [
        ('Additional Info', {
            'fields': ('role', 'bio', 'location', 'website', 'discord_username', 'profile_picture', 
                      'total_points', 'problems_solved', 'contests_participated')
        }),
    ]


class TestCaseInline(admin.TabularInline):
    model = TestCase
    extra = 1


class ProblemAdmin(admin.ModelAdmin):
    list_display = ('title', 'difficulty', 'created_by', 'created_at', 'is_active', 'contest')
    list_filter = ('difficulty', 'is_active', 'created_at', 'contest')
    search_fields = ('title', 'tags')
    inlines = [TestCaseInline]
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class ContestAdmin(admin.ModelAdmin):
    list_display = ('title', 'start_time', 'end_time', 'contest_type', 'difficulty', 'created_by', 'is_active')
    list_filter = ('contest_type', 'difficulty', 'is_active', 'start_time')
    search_fields = ('title', 'description')
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'problem', 'language', 'verdict', 'submitted_at', 'contest')
    list_filter = ('language', 'verdict', 'submitted_at', 'contest')
    search_fields = ('user__username', 'problem__title')
    readonly_fields = ('submitted_at',)


class ContestParticipantAdmin(admin.ModelAdmin):
    list_display = ('user', 'contest', 'score', 'problems_solved', 'registered_at')
    list_filter = ('contest', 'registered_at')
    search_fields = ('user__username', 'contest__title')


class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_by', 'created_at', 'is_active', 'contest')
    list_filter = ('is_active', 'created_at', 'contest')
    search_fields = ('title', 'content')
    
    def save_model(self, request, obj, form, change):
        if not change:  # If creating a new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)


admin.site.register(User, CustomUserAdmin)
admin.site.register(Contest, ContestAdmin)
admin.site.register(Problem, ProblemAdmin)
admin.site.register(TestCase)
admin.site.register(Submission, SubmissionAdmin)
admin.site.register(ContestParticipant, ContestParticipantAdmin)
admin.site.register(UserProblemStatus)
admin.site.register(Announcement, AnnouncementAdmin)
