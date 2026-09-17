from django.contrib import admin
from .models import JobApplication


@admin.register(JobApplication)
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('company', 'job_title', 'job_type', 'status', 'application_date', 'work_mode')
    list_filter = ('status', 'job_type', 'work_mode', 'application_date')
    search_fields = ('company', 'job_title', 'location', 'notes')
    ordering = ('-application_date', '-created_at')
