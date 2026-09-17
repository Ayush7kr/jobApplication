# CareerTrack – Job & Internship Application Tracker Documentation

## 1. Problem Statement
During active hiring seasons, students and job seekers apply to dozens or even hundreds of internships and full-time job openings across platforms like LinkedIn, Indeed, Glassdoor, Unstop, and individual company portals. Candidates struggle to track:
- Which companies they have applied to.
- The status of each application (Applied, Online Assessment, Interview, Selected, Rejected, Withdrawn).
- Application deadlines and interview dates.
- Specific job descriptions, role types, locations, and personal notes.

Without a structured tracking tool, candidates risk missing online assessments, doubling applications, or failing to prepare adequately for upcoming interviews.

---

## 2. Target Users
- **Undergraduate & Graduate Students**: Applying for summer internships, co-ops, and campus recruitment drives.
- **Fresh Graduates**: Seeking entry-level software engineering, data, or technical roles.
- **Job Seekers & Career Changers**: Managing active interview pipelines across multiple companies.

---

## 3. Proposed Solution
**CareerTrack** provides a clean, single-tenant web application dashboard where candidates can manage their job application pipeline. It offers:
- Aggregate dashboard counters for instant visibility into application progress.
- Quick search and filter controls to isolate specific applications by status, job type, or work mode.
- Full Create, Read, Update, and Delete (CRUD) capability.
- Robust client and server-side validation to ensure clean data entry.

---

## 4. Features
1. **Dynamic Dashboard Metrics**: Stat cards displaying Total Applications, Applied, Online Assessment (OA), Interview, Selected, and Rejected counts.
2. **Recent Applications Digest**: Table listing the latest 5 applications for fast status review.
3. **Application Directory**: Full listing with live text search (company/job title) and multi-dropdown filters (Status, Job Type, Work Mode).
4. **Manual HTML Form Interface**: Custom HTML form inputs created without Django Forms/`forms.py` to demonstrate fundamental web request processing.
5. **Detailed View Cards**: Individual detail view showing all position metadata, direct application URLs, timestamps, and formatted notes.
6. **Safe Deletion Flow**: Confirmation dialog step preventing accidental GET deletions.
7. **Responsive Design**: Built using Bootstrap 5 grid utilities, responsive tables, badge components, and clean styling.

---

## 5. Technology Stack
- **Frontend**: HTML5, CSS3, Bootstrap 5.3 (via CDN), Bootstrap Icons.
- **Backend**: Python 3.12, Django 6.1 web framework.
- **Database**: SQLite3 (embedded relation storage).
- **Tooling**: Django test framework (`TestCase`), Django management commands.

---

## 6. Database Structure
The application uses a single main Django model named `JobApplication`:

```python
class JobApplication(models.Model):
    company = models.CharField(max_length=100)
    job_title = models.CharField(max_length=150)
    application_date = models.DateField()
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES, default='Internship')
    location = models.CharField(max_length=100, blank=True, default='')
    work_mode = models.CharField(max_length=20, choices=WORK_MODE_CHOICES, default='Hybrid')
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='Applied')
    application_url = models.URLField(max_length=500, blank=True, default='')
    notes = models.TextField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
```

### Field Explanations:
- `company` & `job_title`: Core identifying text fields.
- `application_date`: Date when candidate submitted application.
- `job_type`: Categorizes employment commitment (Internship, Full-time, Part-time, Contract).
- `location` & `work_mode`: Details office city or arrangement (Remote, Hybrid, On-site).
- `status`: Tracks recruitment pipeline stage (Applied, Online Assessment, Interview, Selected, Rejected, Withdrawn).
- `application_url`: Direct hyperlink to job description or application portal.
- `notes`: Free-form text for interview questions, preparation tips, or contacts.

---

## 7. Workflow Architecture
```
[User Browser]
      │
      │ 1. Submits HTML Form (POST /applications/add/ or /edit/)
      ▼
[Django View: views.py]
      │
      │ 2. Reads request.POST parameters manually
      │ 3. Runs server-side validation logic (_validate_application_data)
      │
      ├── (Validation Failed) ──> Re-renders HTML form with error messages & preserved inputs
      │
      └── (Validation Passed)
            │
            ▼
   [Django Model: models.py] ──> [SQLite DB: db.sqlite3]
            │
            │ 4. ORM saves record to SQLite
            ▼
   [Django View Response]
            │
            │ 5. Triggers Django flash message & HTTP Redirect
            ▼
[User Browser: Application List / Detail Page]
```

---

## 8. CRUD Operations
- **Create**: Navigating to `/applications/add/` loads a manual HTML form. Upon POST submission, `application_create()` validates form values and calls `JobApplication.objects.create()`.
- **Read**:
  - `/` renders top-level aggregate counts and recent entries.
  - `/applications/` queries records with `Q` objects based on search parameters (`q`, `status`, `job_type`, `work_mode`).
  - `/applications/<id>/` retrieves a single instance using `get_object_or_404`.
- **Update**: Navigating to `/applications/<id>/edit/` pre-populates existing model attributes into HTML inputs. On POST submission, `application_update()` validates input, updates instance attributes, and executes `.save()`.
- **Delete**: Navigating to `/applications/<id>/delete/` displays a confirmation warning page. Clicking "Confirm Delete" sends a POST request that triggers `instance.delete()`.

---

## 9. Validation Approach
- **Client-Side Validation**:
  - HTML5 attributes (`required`, `maxlength="100"`, `type="date"`, `type="url"`) provide instant feedback in browser UI before submission.
- **Server-Side Validation**:
  - Implemented manually inside `_validate_application_data(data)` in `views.py`.
  - Validates required fields are non-empty strings.
  - Checks maximum length constraints (company <= 100, job_title <= 150, location <= 100, notes <= 2000).
  - Parses date strings using `datetime.strptime()` to ensure valid YYYY-MM-DD format.
  - Validates choice field membership against allowed tuples.
  - Validates optional URLs using Django's `URLValidator()`.
  - Returns structured error dictionary to re-render form with inline error alerts without losing entered values.

---

## 10. Responsive Design
- **Grid Layout**: Bootstrap 5 breakpoint classes (`col-12`, `col-md-6`, `col-lg-2`, `g-3`) ensure seamless scaling from mobile screens to desktop monitors.
- **Responsive Tables**: Wraps table markup inside `.table-responsive` containers to allow horizontal scrolling on mobile viewports.
- **Status Badges**: Visually distinct Bootstrap contextual badges (`badge-status-applied`, `badge-status-oa`, `badge-status-interview`, `badge-status-selected`, `badge-status-rejected`, `badge-status-withdrawn`) enable quick scanning.

---

## 11. Implementation Challenges
1. **Manual Form Handling without Django Forms**: Operating without `forms.py` required writing custom extraction, validation, error mapping, and input preservation logic.
2. **Filtering Consistency**: Combining search keywords (`Q` OR logic) with multiple select dropdown filters while maintaining filter state across requests.
3. **Database & View Consistency**: Ensuring dynamic counter calculations on the dashboard accurately reflect database changes after creation, editing, or deletion.

---

## 12. Future Scope
- **User Authentication**: Django Auth integration for multi-tenant user account registration and login.
- **Automated Reminders**: Email notifications for upcoming interview dates or assessment submission deadlines.
- **Document Management**: Attachment support for uploading tailored CVs/resumes per application.
- **Analytics & Visualizations**: Charts showing application response rates, funnel conversions, and monthly application frequency.
- **PostgreSQL & Cloud Deployment**: Migration path to PostgreSQL and deployment on AWS/Heroku/Render.

---

## 13. Final Question

**"Why did you choose this solution, and how could it be improved into a real-world product?"**

### Answer:
This solution was chosen because it delivers a clean, lightweight, reliable full-stack application while strictly adhering to core software engineering principles and the screening constraints. By utilizing Django's built-in ORM, SQLite database, and Bootstrap 5 UI framework without third-party JavaScript build overhead (e.g. React/Node), the project remains instantly runnable, performant, easy to understand, and straightforward to maintain.

To evolve CareerTrack into a commercial, production-ready SaaS product:
1. **Multi-Tenancy & Auth**: Add User Authentication (OAuth2 / Google Sign-In) and row-level database security (`user_id` foreign key on `JobApplication`).
2. **Browser Extension Integration**: Build a Chrome Extension to automatically capture job postings from LinkedIn or Indeed with a single click.
3. **Automated Status Sync**: Integrate email parsing (IMAP / Gmail API) to detect confirmation emails and automatically update application statuses (e.g., detecting "assessment invitation" or "interview scheduled").
4. **Cloud Infrastructure**: Deploy on AWS/GCP with PostgreSQL, Redis task queues (Celery) for email reminders, and Docker containerization.
