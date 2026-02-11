# Job Board Platform

[![CI](https://github.com/eliaset/job-board-platform/actions/workflows/ci.yml/badge.svg)](https://github.com/eliaset/job-board-platform/actions/workflows/ci.yml)

A full-stack **Job Board Platform** built with **Django REST Framework** and **React**, featuring role-based access control, JWT authentication, job management, and application tracking.

## 🌐 Live Demo

| Service                | URL                                                                                              |
| ---------------------- | ------------------------------------------------------------------------------------------------ |
| **Frontend**           | [job-board-platform-smoky.vercel.app](https://job-board-platform-smoky.vercel.app)               |
| **Backend API**        | [job-board-api-mxzh.onrender.com](https://job-board-api-mxzh.onrender.com)                       |
| **API Docs (Swagger)** | [job-board-api-mxzh.onrender.com/api/docs/](https://job-board-api-mxzh.onrender.com/api/docs/)   |
| **ReDoc**              | [job-board-api-mxzh.onrender.com/api/redoc/](https://job-board-api-mxzh.onrender.com/api/redoc/) |

### Demo Accounts

| Role     | Email                   | Password       |
| -------- | ----------------------- | -------------- |
| Admin    | `admin@jobboard.com`    | `Admin@123`    |
| Employer | `employer@jobboard.com` | `Employer@123` |

---

## ✨ Features

### Core Features

- **User Authentication** — JWT-based registration, login, profile management
- **Role-Based Access Control** — Admin, Employer, and Job Seeker roles
- **Job Management** — Full CRUD for job postings with categories
- **Application System** — Job seekers apply, employers review and update status
- **Advanced Filtering** — Filter by category, job type, location, salary range
- **Search & Sorting** — Full-text search and multi-field sorting
- **Pagination** — Paginated API responses for large datasets

### Enhanced Features

- **Saved/Bookmarked Jobs** — Users can save and unsave jobs (toggle)
- **Employer Analytics** — Dashboard stats (total jobs, applications, top postings)
- **Seed Data** — Management command to populate demo data
- **API Rate Limiting** — Throttling for security (100/hr anon, 1000/hr auth)
- **Docker Support** — Dockerfile and docker-compose for containerized deployment
- **CI/CD Pipeline** — GitHub Actions for automated testing and linting

---

## 🏗 Tech Stack

| Layer            | Technology                            |
| ---------------- | ------------------------------------- |
| Backend          | Django 5.1, Django REST Framework     |
| Database         | PostgreSQL (prod), SQLite (dev)       |
| Authentication   | JWT (SimpleJWT)                       |
| API Docs         | drf-spectacular (Swagger/OpenAPI 3.0) |
| Frontend         | React 19, Vite, Tailwind CSS          |
| Deployment       | Render (API), Vercel (Frontend)       |
| CI/CD            | GitHub Actions                        |
| Containerization | Docker, Docker Compose                |

---

## 📁 Project Structure

```
job-board-platform/
├── backend/
│   ├── accounts/          # User model, auth views, JWT
│   ├── jobs/              # Job postings, categories, saved jobs
│   ├── applications/      # Job applications, status management
│   ├── config/            # Django settings, root URLs
│   ├── Dockerfile         # Production Docker image
│   ├── build.sh           # Render build script
│   ├── requirements.txt   # Python dependencies
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── components/    # Navbar
│   │   ├── context/       # Auth context (JWT state)
│   │   ├── pages/         # Home, Login, Register, Dashboard, etc.
│   │   └── services/      # API service (Axios + interceptors)
│   └── package.json
├── docker-compose.yml     # Local dev with PostgreSQL
├── render.yaml            # Render deployment blueprint
└── .github/workflows/     # CI/CD pipeline
    └── ci.yml
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.12+
- Node.js 20+
- PostgreSQL (optional — SQLite works for dev)

### Backend Setup

```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: .\venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py create_admin    # Creates admin@jobboard.com
python manage.py seed_data       # Seeds demo categories & jobs
python manage.py runserver
```

### Frontend Setup

```bash
cd frontend
npm install
npm run dev
```

### Docker Setup (Alternative)

```bash
docker-compose up --build
# API at http://localhost:8000
```

---

## 📡 API Endpoints

### Authentication

| Method | Endpoint                   | Description                   |
| ------ | -------------------------- | ----------------------------- |
| POST   | `/api/auth/register/`      | Register (returns JWT tokens) |
| POST   | `/api/auth/login/`         | Login (JWT token pair)        |
| POST   | `/api/auth/token/refresh/` | Refresh access token          |
| GET    | `/api/auth/profile/`       | Get current user profile      |
| PUT    | `/api/auth/profile/`       | Update profile                |

### Jobs

| Method | Endpoint               | Description                                 |
| ------ | ---------------------- | ------------------------------------------- |
| GET    | `/api/jobs/`           | List jobs (filterable, sortable, paginated) |
| POST   | `/api/jobs/`           | Create job (employer/admin)                 |
| GET    | `/api/jobs/{id}/`      | Job detail                                  |
| PUT    | `/api/jobs/{id}/`      | Update job (owner/admin)                    |
| DELETE | `/api/jobs/{id}/`      | Delete job (owner/admin)                    |
| POST   | `/api/jobs/{id}/save/` | Toggle save/unsave job                      |
| GET    | `/api/jobs/saved/`     | List saved jobs                             |
| GET    | `/api/jobs/stats/`     | Employer dashboard stats                    |

### Categories

| Method | Endpoint           | Description             |
| ------ | ------------------ | ----------------------- |
| GET    | `/api/categories/` | List categories         |
| POST   | `/api/categories/` | Create category (admin) |

### Applications

| Method | Endpoint                         | Description                       |
| ------ | -------------------------------- | --------------------------------- |
| POST   | `/api/applications/apply/`       | Apply to job (job seeker)         |
| GET    | `/api/applications/my/`          | My applications (job seeker)      |
| GET    | `/api/applications/job/{id}/`    | Applications for a job (employer) |
| PATCH  | `/api/applications/{id}/status/` | Update application status         |

### Filtering & Search

```
GET /api/jobs/?category=1&job_type=remote&location=Addis&search=engineer&ordering=-salary_max
```

---

## 🔐 Security

- **JWT Authentication** with access/refresh token rotation
- **Role-Based Permissions** — Granular access control per endpoint
- **API Rate Limiting** — 100 req/hr (anonymous), 1000 req/hr (authenticated)
- **CORS** — Configured for frontend domain only
- **Input Validation** — Serializer-level validation on all inputs
- **Unique Constraints** — Prevent duplicate applications and saved jobs

---

## 🧪 Testing

```bash
cd backend
python manage.py test --verbosity=2
```

**27 tests** covering:

- User registration and authentication
- Job CRUD operations and permissions
- Application lifecycle
- Filtering, sorting, and salary validation
- Role-based access control

---

## 🐳 Docker

```bash
# Build and run with PostgreSQL
docker-compose up --build

# Run migrations and seed data
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py create_admin
docker-compose exec web python manage.py seed_data
```

---

## ⚙️ CI/CD

GitHub Actions pipeline runs on every push and PR:

- **Python linting** with flake8
- **Django tests** against PostgreSQL
- **Frontend build** verification

---

## 📊 Database Schema (ERD)

```
┌──────────────┐     ┌───────────────┐     ┌──────────────┐
│     User     │     │  JobCategory  │     │  JobPosting  │
├──────────────┤     ├───────────────┤     ├──────────────┤
│ id (PK)      │     │ id (PK)       │     │ id (PK)      │
│ email        │     │ name          │     │ title        │
│ password     │     │ description   │     │ description  │
│ first_name   │     │ created_at    │     │ company (FK) │──→ User
│ last_name    │     └───────────────┘     │ category(FK) │──→ JobCategory
│ role         │                           │ location     │
│ company_name │     ┌───────────────┐     │ job_type     │
│ bio          │     │JobApplication │     │ salary_min   │
│ phone        │     ├───────────────┤     │ salary_max   │
└──────────────┘     │ id (PK)       │     │ requirements │
       │             │ job (FK)      │──→  │ is_active    │
       │             │ applicant(FK) │──→  │ created_at   │
       │             │ cover_letter  │     │ updated_at   │
       │             │ status        │     └──────────────┘
       │             │ applied_at    │            │
       │             │ updated_at    │     ┌──────────────┐
       │             └───────────────┘     │   SavedJob   │
       │                                   ├──────────────┤
       └───────────────────────────────────│ user (FK)    │
                                           │ job (FK)     │
                                           │ saved_at     │
                                           └──────────────┘
```

---

## 👤 Author

**Elias ET** — ProDev Backend Engineering Program

## 📝 License

This project is part of the ALX ProDev Backend Engineering capstone (Project Nexus).
