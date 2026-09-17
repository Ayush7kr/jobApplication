import os
from datetime import date
from django.test import TestCase, Client
from django.urls import reverse
from django.conf import settings
from .models import JobApplication


class JobApplicationModelTest(TestCase):
    def setUp(self):
        self.app = JobApplication.objects.create(
            company="Google",
            job_title="Software Engineer Intern",
            application_date=date(2026, 9, 1),
            job_type="Internship",
            location="Bangalore",
            work_mode="Hybrid",
            status="Applied",
            application_url="https://careers.google.com",
            notes="Submitted resume"
        )

    def test_str_representation(self):
        self.assertEqual(str(self.app), "Google - Software Engineer Intern")

    def test_model_fields(self):
        self.assertEqual(self.app.company, "Google")
        self.assertEqual(self.app.job_title, "Software Engineer Intern")
        self.assertEqual(self.app.status, "Applied")
        self.assertEqual(self.app.work_mode, "Hybrid")


class DashboardViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        JobApplication.objects.create(
            company="Amazon", job_title="SDE Intern", application_date=date(2026, 9, 2),
            job_type="Internship", status="Applied", work_mode="On-site"
        )
        JobApplication.objects.create(
            company="Microsoft", job_title="SWE Intern", application_date=date(2026, 9, 3),
            job_type="Internship", status="Interview", work_mode="Remote"
        )

    def test_dashboard_url_resolves_and_returns_200(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applications/dashboard.html')
        self.assertEqual(response.context['total_applications'], 2)
        self.assertEqual(response.context['applied_count'], 1)
        self.assertEqual(response.context['interview_count'], 1)


class ApplicationListViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.app1 = JobApplication.objects.create(
            company="Amazon", job_title="SDE Intern", application_date=date(2026, 9, 10),
            job_type="Internship", status="Online Assessment", work_mode="Hybrid"
        )
        self.app2 = JobApplication.objects.create(
            company="Google", job_title="Associate Software Engineer", application_date=date(2026, 9, 11),
            job_type="Full-time", status="Selected", work_mode="Remote"
        )

    def test_application_list_render(self):
        response = self.client.get(reverse('application_list'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Amazon")
        self.assertContains(response, "Google")

    def test_search_filter_by_company_name(self):
        response = self.client.get(reverse('application_list') + '?q=Amazon')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Amazon")
        self.assertNotContains(response, "Google")

    def test_filter_by_status(self):
        response = self.client.get(reverse('application_list') + '?status=Selected')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Google")
        self.assertNotContains(response, "Amazon")

    def test_filter_by_work_mode(self):
        response = self.client.get(reverse('application_list') + '?work_mode=Remote')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Google")
        self.assertNotContains(response, "Amazon")

    def test_combined_search_and_multi_filters(self):
        url = reverse('application_list') + '?q=Engineer&status=Selected&job_type=Full-time&work_mode=Remote'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Google")
        self.assertNotContains(response, "Amazon")


class ApplicationDetailViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.app = JobApplication.objects.create(
            company="Apple", job_title="iOS Engineer", application_date=date(2026, 9, 1),
            job_type="Full-time", status="Interview", work_mode="On-site"
        )

    def test_detail_view_success(self):
        response = self.client.get(reverse('application_detail', args=[self.app.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Apple")
        self.assertContains(response, "iOS Engineer")

    def test_detail_view_404_for_invalid_id(self):
        response = self.client.get(reverse('application_detail', args=[99999]))
        self.assertEqual(response.status_code, 404)


class ApplicationCreateViewTest(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_create_page(self):
        response = self.client.get(reverse('application_create'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'applications/application_form.html')

    def test_post_invalid_data_shows_errors(self):
        # Missing required company and job title, invalid date, invalid choices, invalid URL
        post_data = {
            'company': '',
            'job_title': '',
            'application_date': 'invalid-date',
            'job_type': 'InvalidType',
            'work_mode': 'InvalidMode',
            'status': 'InvalidStatus',
            'application_url': 'ftp://not-a-valid-http-url',
        }
        response = self.client.post(reverse('application_create'), post_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Company name is required.")
        self.assertContains(response, "Job title is required.")
        self.assertContains(response, "Please enter a valid date in YYYY-MM-DD format.")
        self.assertContains(response, "Invalid job type selected.")
        self.assertContains(response, "Invalid work mode selected.")
        self.assertContains(response, "Invalid status selected.")
        self.assertContains(response, "Please enter a valid URL")

    def test_post_valid_data_creates_record(self):
        post_data = {
            'company': 'Netflix',
            'job_title': 'Frontend Engineer Intern',
            'application_date': '2026-09-15',
            'job_type': 'Internship',
            'location': 'Remote',
            'work_mode': 'Remote',
            'status': 'Applied',
            'application_url': 'https://jobs.netflix.com/job/12345',
            'notes': 'Submitted portfolio link.',
        }
        response = self.client.post(reverse('application_create'), post_data)
        self.assertRedirects(response, reverse('application_list'))
        self.assertTrue(JobApplication.objects.filter(company='Netflix', job_title='Frontend Engineer Intern').exists())


class ApplicationUpdateViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.app = JobApplication.objects.create(
            company="Adobe", job_title="SWE Intern", application_date=date(2026, 9, 5),
            job_type="Internship", status="Applied", work_mode="On-site"
        )

    def test_get_edit_form_prepopulated(self):
        response = self.client.get(reverse('application_update', args=[self.app.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Adobe")
        self.assertContains(response, "SWE Intern")

    def test_post_update_status_and_work_mode(self):
        post_data = {
            'company': 'Adobe',
            'job_title': 'SWE Intern',
            'application_date': '2026-09-05',
            'job_type': 'Internship',
            'location': 'Bangalore',
            'work_mode': 'Remote',  # Updated work mode to Remote
            'status': 'Selected',   # Updated status to Selected
            'application_url': 'https://adobe.com/careers',
            'notes': 'Received offer!',
        }
        response = self.client.post(reverse('application_update', args=[self.app.pk]), post_data)
        self.assertRedirects(response, reverse('application_detail', args=[self.app.pk]))

        self.app.refresh_from_db()
        self.assertEqual(self.app.status, 'Selected')
        self.assertEqual(self.app.work_mode, 'Remote')


class ApplicationDeleteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.app = JobApplication.objects.create(
            company="Startup Inc", job_title="Backend Intern", application_date=date(2026, 9, 1),
            job_type="Internship", status="Withdrawn", work_mode="Remote"
        )

    def test_get_confirm_delete_page(self):
        response = self.client.get(reverse('application_delete', args=[self.app.pk]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Startup Inc")
        self.assertContains(response, "Are you sure you want to permanently remove")

    def test_post_deletes_application(self):
        response = self.client.post(reverse('application_delete', args=[self.app.pk]))
        self.assertRedirects(response, reverse('application_list'))
        self.assertFalse(JobApplication.objects.filter(pk=self.app.pk).exists())


class ResponsivenessAndStructureTest(TestCase):
    def setUp(self):
        self.client = Client()
        JobApplication.objects.create(
            company="TestCorp", job_title="Engineer", application_date=date(2026, 9, 1),
            job_type="Full-time", status="Applied", work_mode="Remote"
        )

    def test_meta_viewport_and_bootstrap_responsive_classes(self):
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, '<meta name="viewport" content="width=device-width, initial-scale=1.0">')
        self.assertContains(response, 'table-responsive')


class NoFormsPyConstraintTest(TestCase):
    def test_forms_py_does_not_exist(self):
        app_dir = os.path.dirname(os.path.abspath(__file__))
        forms_py_path = os.path.join(app_dir, 'forms.py')
        self.assertFalse(
            os.path.exists(forms_py_path),
            "Requirement violation: forms.py should not exist in the codebase."
        )
