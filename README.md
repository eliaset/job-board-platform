# 💼 Job Board Platform

A full-stack **Job Board Platform** with a robust RESTful backend API built with **Django REST Framework** and a modern React frontend. Features role-based access control, job posting management, application tracking, and comprehensive API documentation.

---

## 🚀 Tech Stack

### Backend

| Technology                | Purpose                                    |
| ------------------------- | ------------------------------------------ |
| **Django 5.1**            | Web framework                              |
| **Django REST Framework** | Building RESTful APIs                      |
| **PostgreSQL**            | Production database (SQLite for local dev) |
| **JWT (SimpleJWT)**       | Secure authentication                      |
| **drf-spectacular**       | Swagger/OpenAPI documentation              |
| **django-filter**         | Advanced filtering                         |
| **Gunicorn**              | Production WSGI server                     |

### Frontend

| Technology       | Purpose                     |
| ---------------- | --------------------------- |
| **React**        | UI framework                |
| **Vite**         | Build tool                  |
| **Tailwind CSS** | Utility-first CSS framework |

---

## 📊 Entity-Relationship Diagram

```mermaid
erDiagram
    USER {
        int id PK
        string email UK
        string first_name
        string last_name
        string role "admin | employer | job_seeker"
        string company_name
        string bio
        string phone
        datetime date_joined
    }

    JOB_CATEGORY {
        int id PK
        string name UK
        string description
        datetime created_at
    }

    JOB_POSTING {
        int id PK
        string title
        text description
        int company_id FK
        int category_id FK
        string location
        string job_type "full_time | part_time | contract | remote | internship"
        decimal salary_min
        decimal salary_max
        text requirements
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    JOB_APPLICATION {
        int id PK
        int job_id FK
        int applicant_id FK
        text cover_letter
        string status "pending | reviewed | accepted | rejected"
        datetime applied_at
        datetime updated_at
    }

    USER ||--o{ JOB_POSTING : "posts (employer)"
    JOB_CATEGORY ||--o{ JOB_POSTING : "categorizes"
    JOB_POSTING ||--o{ JOB_APPLICATION : "receives"
    USER ||--o{ JOB_APPLICATION : "submits (job_seeker)"
```

---

## 🔐 Role-Based Access Control

| Role           | Capabilities                                                     |
| -------------- | ---------------------------------------------------------------- |
| **Admin**      | Manage categories, all jobs, all applications, all users         |
| **Employer**   | Create/manage own job postings, review applications for own jobs |
| **Job Seeker** | Browse jobs, apply to jobs, view own applications                |

---

## 📡 API Endpoints

### Authentication (`/api/auth/`)

| Method    | Endpoint          | Access        | Description          |
| --------- | ----------------- | ------------- | -------------------- |
| `POST`    | `/register/`      | Public        | Register new user    |
| `POST`    | `/login/`         | Public        | Obtain JWT tokens    |
| `POST`    | `/token/refresh/` | Authenticated | Refresh access token |
| `GET/PUT` | `/profile/`       | Authenticated | View/update profile  |

### Job Categories (`/api/categories/`)

| Method       | Endpoint | Access | Description            |
| ------------ | -------- | ------ | ---------------------- |
| `GET`        | `/`      | Public | List all categories    |
| `POST`       | `/`      | Admin  | Create category        |
| `GET`        | `/{id}/` | Public | Category detail        |
| `PUT/DELETE` | `/{id}/` | Admin  | Update/delete category |

### Job Postings (`/api/jobs/`)

| Method       | Endpoint | Access         | Description                                 |
| ------------ | -------- | -------------- | ------------------------------------------- |
| `GET`        | `/`      | Public         | List jobs (filterable, sortable, paginated) |
| `POST`       | `/`      | Employer/Admin | Create job posting                          |
| `GET`        | `/{id}/` | Public         | Job detail                                  |
| `PUT/DELETE` | `/{id}/` | Owner/Admin    | Update/delete job                           |

**Filters:** `category`, `job_type`, `location`, `salary_min`, `salary_max`, `is_active`
**Sorting:** `created_at`, `salary_min`, `salary_max`, `title`
**Search:** `title`, `description`, `location`

### Job Applications (`/api/applications/`)

| Method  | Endpoint         | Access           | Description                 |
| ------- | ---------------- | ---------------- | --------------------------- |
| `POST`  | `/apply/`        | Job Seeker       | Apply to a job              |
| `GET`   | `/my/`           | Job Seeker       | View own applications       |
| `GET`   | `/job/{job_id}/` | Employer (owner) | View applications for a job |
| `PATCH` | `/{id}/status/`  | Employer (owner) | Update application status   |

### API Documentation

| Endpoint       | Description                                    |
| -------------- | ---------------------------------------------- |
| `/api/docs/`   | **Swagger UI** — Interactive API documentation |
| `/api/redoc/`  | **ReDoc** — Alternative API documentation      |
| `/api/schema/` | OpenAPI 3.0 JSON schema                        |

---

## ⚙️ Local Development Setup

### Prerequisites

- Python 3.10+
- Node.js 18+ & npm
- PostgreSQL (optional — SQLite used by default for local dev)

### Backend Setup

```bash
cd backend

# Create and activate virtual environment
python -m venv venv
# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run migrations
python manage.py migrate

# Create a superuser (admin)
python manage.py createsuperuser

# Start the development server
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend

# Install dependencies
npm install

# Start the development server
npm run dev
```

### Environment Variables (optional `backend/.env` file)

```env
SECRET_KEY=your-secret-key
DEBUG=True
DATABASE_URL=postgresql://user:password@localhost:5432/job_board
ALLOWED_HOSTS=localhost,127.0.0.1
```

---

## 🧪 Testing

```bash
cd backend
python manage.py test
```

---

## 🌐 Deployment (Render)

The backend includes a `render.yaml` blueprint for one-click deployment:

1. Push code to GitHub
2. Go to [Render Dashboard](https://dashboard.render.com)
3. Click **New → Blueprint** and connect your GitHub repo
4. Render will automatically provision a PostgreSQL database and deploy the API

---

## 📁 Project Structure

```
job-board-platform/
├── backend/                 # Django REST API
│   ├── config/              # Django project configuration
│   │   ├── settings.py      # Settings (DB, auth, REST, Swagger)
│   │   ├── urls.py          # Main URL routing
│   │   └── wsgi.py          # WSGI entry point
│   ├── accounts/            # User authentication & profiles
│   │   ├── models.py        # Custom User model with roles
│   │   ├── serializers.py   # Registration, profile serializers
│   │   ├── views.py         # Auth views (register, login, profile)
│   │   ├── permissions.py   # Role-based permission classes
│   │   └── urls.py          # Auth URL patterns
│   ├── jobs/                # Job postings & categories
│   │   ├── models.py        # JobCategory, JobPosting models
│   │   ├── serializers.py   # Job serializers
│   │   ├── views.py         # Job CRUD views
│   │   ├── filters.py       # Django-filter filter sets
│   │   └── admin.py         # Admin panel config
│   ├── applications/        # Job applications
│   │   ├── models.py        # JobApplication model
│   │   ├── serializers.py   # Application serializers
│   │   ├── views.py         # Application views
│   │   └── urls.py          # Application URL patterns
│   ├── requirements.txt     # Python dependencies
│   ├── Procfile             # Gunicorn entry point
│   ├── render.yaml          # Render deployment blueprint
│   └── manage.py            # Django management script
├── frontend/                # React + Vite + Tailwind CSS
├── .gitignore
└── README.md
```

---

## 👨‍💻 Author

Built as part of **Project Nexus** — ProDev Backend Engineering Program.

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
