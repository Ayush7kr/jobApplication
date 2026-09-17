# CareerTrack – Job & Internship Application Tracker

CareerTrack is a full-stack web application designed for students, fresh graduates, and job seekers to track, organize, and manage their job and internship applications in one centralized dashboard.

---

## 1. Problem Statement
Students and job seekers frequently apply to dozens of internships and job openings across multiple job boards (LinkedIn, Indeed, Unstop, company career pages). Managing application dates, interview schedules, status updates (Online Assessment, Interview, Offer), application links, and notes using spreadsheets or physical notebooks is error-prone, disorganized, and tedious.

## 2. Target Users
- College students applying for summer/winter internships.
- Fresh graduates looking for entry-level engineering/software roles.
- Active job seekers managing multiple ongoing interview pipelines.

## 3. Key Features
- **Interactive Dashboard**: Real-time counter metrics for Total Applications, Applied, Online Assessments (OA), Interviews, Selected, and Rejected.
- **Application Directory**: Search applications by company or job title; filter by Status, Job Type, or Work Mode.
- **Full CRUD Operations**: Create, View, Edit, and Delete job applications with safety confirmation steps.
- **Manual Form Processing**: Custom HTML forms built without Django Forms framework to demonstrate raw HTTP `request.POST` handling.
- **Dual Validation**: HTML5 client-side attributes (`required`, `type="url"`, `type="date"`) paired with strict server-side validation in Django views.
- **Responsive Bootstrap 5 UI**: Fully mobile-responsive table grids, stat cards, badges, and modal dialogs.
- **Sample Data Generator**: Management command (`python manage.py populate_sample_data`) to quickly seed realistic test data.

## 4. Technology Stack
- **Backend Framework**: Python 3.12, Django 6.1
- **Database**: SQLite3
- **Frontend**: HTML5, Vanilla CSS3, Bootstrap 5.3 (via CDN), Bootstrap Icons
- **Strict Constraints**: No React, Angular, Vue, Node.js, DRF, or Django `forms.py`.

## 5. Database Structure
The project uses a single primary model called `JobApplication` stored in SQLite:

| Field Name | Type | Constraints / Details |
| :--- | :--- | :--- |
| `id` | AutoField | Primary Key |
| `company` | CharField | Required, max 100 chars |
| `job_title` | CharField | Required, max 150 chars |
| `application_date` | DateField | Required |
| `job_type` | CharField | Choices: `Internship`, `Full-time`, `Part-time`, `Contract` |
| `location` | CharField | Optional (`blank=True`), max 100 chars |
| `work_mode` | CharField | Choices: `Remote`, `Hybrid`, `On-site` |
| `status` | CharField | Choices: `Applied`, `Online Assessment`, `Interview`, `Selected`, `Rejected`, `Withdrawn` |
| `application_url` | URLField | Optional (`blank=True`), max 500 chars |
| `notes` | TextField | Optional (`blank=True`), max 2000 chars |
| `created_at` | DateTimeField | Auto timestamp on creation |
| `updated_at` | DateTimeField | Auto timestamp on update |

## 6. Application Workflow
```
User (Browser)
   │
   ├──> 1. Submits HTML Form (POST /applications/add/ or /edit/)
   │
Django View (`views.py`)
   │
   ├──> 2. Extracts request.POST parameters manually
   ├──> 3. Executes `_validate_application_data()` (Server Validation)
   │       ├── Invalid? ──> Re-renders HTML form with error alerts & preserves input
   │       └── Valid? ────> Proceeds to ORM operations
   │
Django Model (`models.py`)
   │
   ├──> 4. `JobApplication.objects.create()` / `.save()` ──> Persists to SQLite (`db.sqlite3`)
   │
Django View Response
   │
   └──> 5. Triggers Django Messages Framework & Redirects User to UI
```

## 7. Project Structure
```
careertrack/
│
├── manage.py                   # Django management script
├── requirements.txt            # Python dependencies
├── .gitignore                  # Git ignore rules
├── README.md                   # Primary project documentation
├── db.sqlite3                  # SQLite database
│
├── careertrack/                # Core Django configuration
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   └── wsgi.py
│
├── applications/               # Application Tracker Django app
│   ├── migrations/             # Database migration files
│   ├── static/
│   │   └── applications/
│   │       └── style.css       # Custom stylesheet & status badges
│   ├── templates/
│   │   └── applications/
│   │       ├── base.html                   # Base layout template
│   │       ├── dashboard.html              # Metric cards & recent apps
│   │       ├── application_list.html       # Search, filter & main table
│   │       ├── application_detail.html     # Single application view
│   │       ├── application_form.html       # Add & Edit HTML form
│   │       └── application_confirm_delete.html # Safe delete confirmation
│   ├── admin.py                # Django Admin registration
│   ├── apps.py
│   ├── models.py               # JobApplication model
│   ├── tests.py                # Automated unit tests
│   ├── urls.py                 # App-level routing
│   ├── views.py                # Business logic & manual form handling
│   └── management/
│       └── commands/
│           └── populate_sample_data.py # Sample data CLI command
│
└── docs/
    └── project_documentation.md # Technical screening documentation
```

## 8. Installation Instructions
1. **Clone or navigate to repository directory**:
   ```bash
   cd f:/screening_task
   ```
2. **Install Python dependencies**:
   ```bash
   python -m pip install -r requirements.txt
   ```

## 9. How to Run Locally
1. **Apply Database Migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```
2. **(Optional) Seed Realistic Sample Data**:
   ```bash
   python manage.py populate_sample_data
   ```
3. **Run Unit Tests**:
   ```bash
   python manage.py test
   ```
4. **Start Django Development Server**:
   ```bash
   python manage.py runserver
   ```
5. **Open Application in Browser**:
   Navigate to `http://127.0.0.1:8000/`.

## 10. CRUD Implementation Summary
- **Create**: Route `/applications/add/` processes `request.POST` data manually, runs server-side validation, and executes `JobApplication.objects.create()`.
- **Read**: Route `/` displays summary statistics and recent entries. Route `/applications/` lists all records with filtering and search (`Q` objects). Route `/applications/<id>/` displays a detailed single record card.
- **Update**: Route `/applications/<id>/edit/` pre-populates existing model values in HTML form controls and updates fields via `instance.save()`.
- **Delete**: Route `/applications/<id>/delete/` presents a GET confirmation page and executes safe POST deletion via `instance.delete()`.

## 11. Validation Approach
- **Client-Side Validation**: Enforced directly in browser HTML using attributes `required`, `maxlength="100"`, `type="date"`, and `type="url"`.
- **Server-Side Validation**: Handled in Python inside `_validate_application_data(data)` within `views.py`. Checks non-emptiness of required fields, string length bounds, valid date parsing (`strptime`), choice membership, and valid URL structure (`URLValidator`). If validation fails, errors are returned to the template along with submitted values to preserve user input.

## 12. Challenges Faced
- **Manual Form Handling without Django Forms**: Extracting, sanitizing, validating, and re-rendering field errors without `forms.py` required writing a dedicated validation helper (`_validate_application_data`) and carefully wiring form `value` attributes in HTML.
- **Dynamic Status Metrics**: Aggregating distinct application statuses efficiently using Django ORM `.filter(status=...).count()`.

## 13. Future Scope
- User authentication and multi-user data isolation.
- Automated email and calendar notifications for upcoming interviews or OA deadlines.
- Resume/CV upload attachment linked to each application.
- Advanced visual analytics (application response rates, timeline charts).

## 14. Why This Solution Was Chosen
Choosing Django with SQLite and Bootstrap 5 provided a clean, robust, and readable architectural stack. By maintaining zero complex frontend build steps (npm, webpack, node_modules), the project is lightweight, portable, easy to audit, and instantly runnable for interview evaluation.
