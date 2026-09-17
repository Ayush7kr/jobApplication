from datetime import date, timedelta
from django.core.management.base import BaseCommand
from applications.models import JobApplication


class Command(BaseCommand):
    help = 'Populates the SQLite database with realistic sample job application records.'

    def handle(self, *args, **options):
        self.stdout.write('Populating sample job applications...')

        sample_apps = [
            {
                'company': 'Amazon',
                'job_title': 'Software Development Engineer Intern',
                'application_date': date.today() - timedelta(days=12),
                'job_type': 'Internship',
                'location': 'Bangalore',
                'work_mode': 'Hybrid',
                'status': 'Online Assessment',
                'application_url': 'https://amazon.jobs/en/jobs/2849201/sde-intern',
                'notes': 'Completed Hackerrank assessment on 10th Sept. Passed 2/2 problem sets. Waiting for recruiter review.',
            },
            {
                'company': 'Microsoft',
                'job_title': 'Software Engineer Intern',
                'application_date': date.today() - timedelta(days=20),
                'job_type': 'Internship',
                'location': 'Hyderabad',
                'work_mode': 'Hybrid',
                'status': 'Interview',
                'application_url': 'https://careers.microsoft.com/us/en/job/1749102/swe-intern',
                'notes': 'Technical Round 1 scheduled for next Monday. Focusing on Data Structures, Algorithms, and System Design basics.',
            },
            {
                'company': 'Google',
                'job_title': 'Associate Software Engineer',
                'application_date': date.today() - timedelta(days=5),
                'job_type': 'Full-time',
                'location': 'Bangalore',
                'work_mode': 'On-site',
                'status': 'Applied',
                'application_url': 'https://careers.google.com/jobs/results/9301923-associate-software-engineer/',
                'notes': 'Submitted application via employee referral from college alumnus.',
            },
            {
                'company': 'TCS',
                'job_title': 'Graduate Engineer Trainee',
                'application_date': date.today() - timedelta(days=35),
                'job_type': 'Full-time',
                'location': 'Pune',
                'work_mode': 'On-site',
                'status': 'Selected',
                'application_url': 'https://www.tcs.com/careers/entry-level',
                'notes': 'Received official offer letter via campus placement portal. Joining date scheduled for July 2027.',
            },
            {
                'company': 'Infosys',
                'job_title': 'Systems Engineer',
                'application_date': date.today() - timedelta(days=40),
                'job_type': 'Full-time',
                'location': 'Mysore',
                'work_mode': 'On-site',
                'status': 'Selected',
                'application_url': 'https://www.infosys.com/careers/freshers.html',
                'notes': 'Offer confirmed following InfyTQ test and technical discussion.',
            },
            {
                'company': 'Meta',
                'job_title': 'Front End Engineer Intern',
                'application_date': date.today() - timedelta(days=18),
                'job_type': 'Internship',
                'location': 'London / Remote',
                'work_mode': 'Remote',
                'status': 'Rejected',
                'application_url': 'https://www.metacareers.com/v2/jobs/928104812/',
                'notes': 'Application status updated to position closed. Will re-apply next hiring cycle.',
            },
            {
                'company': 'Adobe',
                'job_title': 'Software Quality Engineer Intern',
                'application_date': date.today() - timedelta(days=8),
                'job_type': 'Internship',
                'location': 'Noida',
                'work_mode': 'Hybrid',
                'status': 'Applied',
                'application_url': 'https://adobe.wd5.myworkdayjobs.com/external_experienced/job/Noida/SWE-Intern_R14920',
                'notes': 'Applied directly on company career site.',
            },
            {
                'company': 'Netflix',
                'job_title': 'Full Stack Software Engineer (New Grad)',
                'application_date': date.today() - timedelta(days=25),
                'job_type': 'Full-time',
                'location': 'Remote',
                'work_mode': 'Remote',
                'status': 'Withdrawn',
                'application_url': 'https://jobs.netflix.com/jobs/8291039',
                'notes': 'Withdrew application due to geographical location restriction.',
            }
        ]

        created_count = 0
        for item in sample_apps:
            obj, created = JobApplication.objects.get_or_create(
                company=item['company'],
                job_title=item['job_title'],
                defaults=item
            )
            if created:
                created_count += 1

        self.stdout.write(self.style.SUCCESS(f'Successfully created {created_count} sample job application records!'))
