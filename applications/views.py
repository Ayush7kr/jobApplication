from datetime import datetime
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.db.models import Q

from .models import JobApplication


def dashboard(request):
    """
    Renders the application dashboard with dynamic status statistics
    and recent applications table.
    """
    total_applications = JobApplication.objects.count()
    applied_count = JobApplication.objects.filter(status='Applied').count()
    oa_count = JobApplication.objects.filter(status='Online Assessment').count()
    interview_count = JobApplication.objects.filter(status='Interview').count()
    selected_count = JobApplication.objects.filter(status='Selected').count()
    rejected_count = JobApplication.objects.filter(status='Rejected').count()

    recent_applications = JobApplication.objects.all()[:5]

    context = {
        'total_applications': total_applications,
        'applied_count': applied_count,
        'oa_count': oa_count,
        'interview_count': interview_count,
        'selected_count': selected_count,
        'rejected_count': rejected_count,
        'recent_applications': recent_applications,
    }
    return render(request, 'applications/dashboard.html', context)


def application_list(request):
    """
    Renders all applications with multi-criteria search and filter options.
    """
    search_query = request.GET.get('q', '').strip()
    status_filter = request.GET.get('status', '').strip()
    job_type_filter = request.GET.get('job_type', '').strip()
    work_mode_filter = request.GET.get('work_mode', '').strip()

    applications = JobApplication.objects.all()

    if search_query:
        applications = applications.filter(
            Q(company__icontains=search_query) | Q(job_title__icontains=search_query)
        )

    if status_filter and status_filter != 'All':
        applications = applications.filter(status=status_filter)

    if job_type_filter and job_type_filter != 'All':
        applications = applications.filter(job_type=job_type_filter)

    if work_mode_filter and work_mode_filter != 'All':
        applications = applications.filter(work_mode=work_mode_filter)

    context = {
        'applications': applications,
        'search_query': search_query,
        'selected_status': status_filter or 'All',
        'selected_job_type': job_type_filter or 'All',
        'selected_work_mode': work_mode_filter or 'All',
        'status_choices': [choice[0] for choice in JobApplication.STATUS_CHOICES],
        'job_type_choices': [choice[0] for choice in JobApplication.JOB_TYPE_CHOICES],
        'work_mode_choices': [choice[0] for choice in JobApplication.WORK_MODE_CHOICES],
    }
    return render(request, 'applications/application_list.html', context)


def application_detail(request, pk):
    """
    Displays full details of a specific job application.
    """
    application = get_object_or_404(JobApplication, pk=pk)
    return render(request, 'applications/application_detail.html', {'application': application})


def _validate_application_data(data):
    """
    Helper function to validate application form data server-side.
    Returns a dictionary of error messages (empty if valid).
    """
    errors = {}

    company = data.get('company', '').strip()
    job_title = data.get('job_title', '').strip()
    application_date = data.get('application_date', '').strip()
    job_type = data.get('job_type', '').strip()
    location = data.get('location', '').strip()
    work_mode = data.get('work_mode', '').strip()
    status = data.get('status', '').strip()
    application_url = data.get('application_url', '').strip()
    notes = data.get('notes', '').strip()

    # Company validation
    if not company:
        errors['company'] = 'Company name is required.'
    elif len(company) > 100:
        errors['company'] = 'Company name cannot exceed 100 characters.'

    # Job title validation
    if not job_title:
        errors['job_title'] = 'Job title is required.'
    elif len(job_title) > 150:
        errors['job_title'] = 'Job title cannot exceed 150 characters.'

    # Application date validation
    if not application_date:
        errors['application_date'] = 'Application date is required.'
    else:
        try:
            datetime.strptime(application_date, '%Y-%m-%d')
        except ValueError:
            errors['application_date'] = 'Please enter a valid date in YYYY-MM-DD format.'

    # Job type validation
    valid_job_types = [choice[0] for choice in JobApplication.JOB_TYPE_CHOICES]
    if not job_type:
        errors['job_type'] = 'Job type is required.'
    elif job_type not in valid_job_types:
        errors['job_type'] = f'Invalid job type selected. Choose from: {", ".join(valid_job_types)}.'

    # Work mode validation
    valid_work_modes = [choice[0] for choice in JobApplication.WORK_MODE_CHOICES]
    if not work_mode:
        errors['work_mode'] = 'Work mode is required.'
    elif work_mode not in valid_work_modes:
        errors['work_mode'] = f'Invalid work mode selected. Choose from: {", ".join(valid_work_modes)}.'

    # Status validation
    valid_statuses = [choice[0] for choice in JobApplication.STATUS_CHOICES]
    if not status:
        errors['status'] = 'Application status is required.'
    elif status not in valid_statuses:
        errors['status'] = f'Invalid status selected. Choose from: {", ".join(valid_statuses)}.'

    # Location length validation
    if len(location) > 100:
        errors['location'] = 'Location cannot exceed 100 characters.'

    # URL validation
    if application_url:
        validator = URLValidator()
        try:
            validator(application_url)
        except ValidationError:
            errors['application_url'] = 'Please enter a valid URL (e.g. https://example.com/job).'

    # Notes length validation
    if len(notes) > 2000:
        errors['notes'] = 'Notes cannot exceed 2000 characters.'

    return errors


def application_create(request):
    """
    Handles manually created HTML form for adding a new job application.
    Does NOT use Django Forms or forms.py.
    """
    if request.method == 'POST':
        form_data = {
            'company': request.POST.get('company', '').strip(),
            'job_title': request.POST.get('job_title', '').strip(),
            'application_date': request.POST.get('application_date', '').strip(),
            'job_type': request.POST.get('job_type', '').strip(),
            'location': request.POST.get('location', '').strip(),
            'work_mode': request.POST.get('work_mode', '').strip(),
            'status': request.POST.get('status', '').strip(),
            'application_url': request.POST.get('application_url', '').strip(),
            'notes': request.POST.get('notes', '').strip(),
        }

        errors = _validate_application_data(form_data)

        if errors:
            messages.error(request, 'Please fix the errors indicated below.')
            context = {
                'form_data': form_data,
                'errors': errors,
                'job_type_choices': JobApplication.JOB_TYPE_CHOICES,
                'work_mode_choices': JobApplication.WORK_MODE_CHOICES,
                'status_choices': JobApplication.STATUS_CHOICES,
                'title': 'Add Job Application',
                'is_edit': False,
            }
            return render(request, 'applications/application_form.html', context)

        # Parse date and save instance manually using ORM
        app_date = datetime.strptime(form_data['application_date'], '%Y-%m-%d').date()
        application = JobApplication.objects.create(
            company=form_data['company'],
            job_title=form_data['job_title'],
            application_date=app_date,
            job_type=form_data['job_type'],
            location=form_data['location'],
            work_mode=form_data['work_mode'],
            status=form_data['status'],
            application_url=form_data['application_url'],
            notes=form_data['notes'],
        )

        messages.success(request, f"Application for '{application.company} - {application.job_title}' added successfully!")
        return redirect('application_list')

    # GET request - render blank form
    context = {
        'form_data': {'application_date': datetime.now().strftime('%Y-%m-%d')},
        'errors': {},
        'job_type_choices': JobApplication.JOB_TYPE_CHOICES,
        'work_mode_choices': JobApplication.WORK_MODE_CHOICES,
        'status_choices': JobApplication.STATUS_CHOICES,
        'title': 'Add Job Application',
        'is_edit': False,
    }
    return render(request, 'applications/application_form.html', context)


def application_update(request, pk):
    """
    Handles manually created HTML form for editing an existing job application.
    Does NOT use Django Forms or forms.py.
    """
    application = get_object_or_404(JobApplication, pk=pk)

    if request.method == 'POST':
        form_data = {
            'company': request.POST.get('company', '').strip(),
            'job_title': request.POST.get('job_title', '').strip(),
            'application_date': request.POST.get('application_date', '').strip(),
            'job_type': request.POST.get('job_type', '').strip(),
            'location': request.POST.get('location', '').strip(),
            'work_mode': request.POST.get('work_mode', '').strip(),
            'status': request.POST.get('status', '').strip(),
            'application_url': request.POST.get('application_url', '').strip(),
            'notes': request.POST.get('notes', '').strip(),
        }

        errors = _validate_application_data(form_data)

        if errors:
            messages.error(request, 'Please fix the errors indicated below.')
            context = {
                'application': application,
                'form_data': form_data,
                'errors': errors,
                'job_type_choices': JobApplication.JOB_TYPE_CHOICES,
                'work_mode_choices': JobApplication.WORK_MODE_CHOICES,
                'status_choices': JobApplication.STATUS_CHOICES,
                'title': f'Edit Application - {application.company}',
                'is_edit': True,
            }
            return render(request, 'applications/application_form.html', context)

        # Update application attributes
        application.company = form_data['company']
        application.job_title = form_data['job_title']
        application.application_date = datetime.strptime(form_data['application_date'], '%Y-%m-%d').date()
        application.job_type = form_data['job_type']
        application.location = form_data['location']
        application.work_mode = form_data['work_mode']
        application.status = form_data['status']
        application.application_url = form_data['application_url']
        application.notes = form_data['notes']
        application.save()

        messages.success(request, f"Application for '{application.company}' updated successfully!")
        return redirect('application_detail', pk=application.pk)

    # GET request - pre-populate form with existing database values
    form_data = {
        'company': application.company,
        'job_title': application.job_title,
        'application_date': application.application_date.strftime('%Y-%m-%d') if application.application_date else '',
        'job_type': application.job_type,
        'location': application.location,
        'work_mode': application.work_mode,
        'status': application.status,
        'application_url': application.application_url,
        'notes': application.notes,
    }

    context = {
        'application': application,
        'form_data': form_data,
        'errors': {},
        'job_type_choices': JobApplication.JOB_TYPE_CHOICES,
        'work_mode_choices': JobApplication.WORK_MODE_CHOICES,
        'status_choices': JobApplication.STATUS_CHOICES,
        'title': f'Edit Application - {application.company}',
        'is_edit': True,
    }
    return render(request, 'applications/application_form.html', context)


def application_delete(request, pk):
    """
    Renders confirmation page on GET and executes safe deletion on POST.
    """
    application = get_object_or_404(JobApplication, pk=pk)

    if request.method == 'POST':
        company_name = application.company
        title_name = application.job_title
        application.delete()
        messages.success(request, f"Application for '{company_name} - {title_name}' deleted successfully.")
        return redirect('application_list')

    return render(request, 'applications/application_confirm_delete.html', {'application': application})
