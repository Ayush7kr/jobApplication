from django.db import models


class JobApplication(models.Model):
    """
    Model representing a job or internship application.
    Tracks company, position details, application date, work mode, status, and custom notes.
    """

    JOB_TYPE_CHOICES = (
        ('Internship', 'Internship'),
        ('Full-time', 'Full-time'),
        ('Part-time', 'Part-time'),
        ('Contract', 'Contract'),
    )

    WORK_MODE_CHOICES = (
        ('Remote', 'Remote'),
        ('Hybrid', 'Hybrid'),
        ('On-site', 'On-site'),
    )

    STATUS_CHOICES = (
        ('Applied', 'Applied'),
        ('Online Assessment', 'Online Assessment'),
        ('Interview', 'Interview'),
        ('Selected', 'Selected'),
        ('Rejected', 'Rejected'),
        ('Withdrawn', 'Withdrawn'),
    )

    company = models.CharField(max_length=100, help_text="Company name (max 100 characters)")
    job_title = models.CharField(max_length=150, help_text="Job role or position title (max 150 characters)")
    application_date = models.DateField(help_text="Date when application was submitted")
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='Internship')
    location = models.CharField(max_length=100, blank=True, default='', help_text="Location e.g. Bangalore, Remote")
    work_mode = models.CharField(max_length=20, choices=WORK_MODE_CHOICES, default='Hybrid')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Applied')
    application_url = models.URLField(max_length=500, blank=True, default='', help_text="Direct link to job posting or application portal")
    notes = models.TextField(blank=True, default='', help_text="Additional notes e.g. interview stages, contact details")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-application_date', '-created_at']

    def __str__(self):
        return f"{self.company} - {self.job_title}"
