# Job Board Platform — Presentation Slides Outline

> Transfer this outline to **Google Slides**. Each section = 1 slide.

---

## Slide 1: Title Slide

**Job Board Platform**
Full-Stack REST API with Django & React

- Name: Elias ET
- Program: ALX ProDev Backend Engineering
- Project Nexus — February 2026

---

## Slide 2: Problem & Solution

**Problem:** Job seekers and employers need a centralized, efficient platform to connect.

**Solution:** A full-stack Job Board with:

- Role-based access (Admin, Employer, Job Seeker)
- RESTful API with filtering, search, and pagination
- JWT authentication for secure access
- Real-time application tracking

---

## Slide 3: Tech Stack

| Layer            | Technology                        |
| ---------------- | --------------------------------- |
| Backend          | Django 5.1, Django REST Framework |
| Database         | PostgreSQL                        |
| Auth             | JWT (SimpleJWT)                   |
| API Docs         | Swagger / OpenAPI 3.0             |
| Frontend         | React 19, Vite, Tailwind CSS      |
| Deployment       | Render (API) + Vercel (Frontend)  |
| CI/CD            | GitHub Actions                    |
| Containerization | Docker                            |

---

## Slide 4: Architecture Diagram

- **Frontend (Vercel)** → HTTPS → **Backend API (Render)** → **PostgreSQL (Render)**
- JWT tokens flow between frontend and backend
- GitHub Actions CI pipeline on every push
- Docker for local development

---

## Slide 5: Database Design (ERD)

_(Insert the ERD image here)_

**5 Models:**

- User (3 roles), JobCategory, JobPosting, JobApplication, SavedJob
- Normalized schema with proper foreign keys
- Composite unique constraints prevent duplicate applications/saves
- Database indexes on frequently queried fields

---

## Slide 6: Key API Endpoints

**Auth:** Register, Login, Token Refresh, Profile

**Jobs:** CRUD + Filter by category, type, location, salary + Search + Sort + Paginate

**Applications:** Apply, My Applications, Job Applications, Update Status

**Bonus:** Toggle Save Job, List Saved Jobs, Employer Stats/Analytics

> Full interactive docs at `/api/docs/` (Swagger UI)

---

## Slide 7: Security & Best Practices

- **JWT Authentication** — Stateless, secure token-based auth
- **Role-Based Access Control** — Permission classes per endpoint
- **API Rate Limiting** — 100/hr anonymous, 1000/hr authenticated
- **CORS** — Restricted to frontend domain only
- **Input Validation** — Serializer-level validation
- **Unique Constraints** — DB-level duplicate prevention
- **27 Unit Tests** — Automated with CI/CD

---

## Slide 8: Deployment & DevOps

- **Render** — Backend API with PostgreSQL
- **Vercel** — Frontend static site with CDN
- **Docker** — Dockerfile + docker-compose for local dev
- **GitHub Actions CI/CD** — Auto test + lint on every push
- **Management Commands** — `create_admin`, `seed_data` for reproducible setup

---

## Slide 9: Live Demo

_(Switch to browser — show the running application)_

1. Browse jobs on homepage (filtering, search)
2. Register as a job seeker → auto-login
3. View job detail → apply
4. Login as employer → post a new job
5. Check employer dashboard → see applications
6. Show Swagger docs at `/api/docs/`

---

## Slide 10: Challenges & Lessons Learned

- **CORS Configuration** — Learned about cross-origin security between Vercel/Render
- **Render Deployment** — Blueprint YAML configuration and static site limitations
- **JWT Token Flow** — Implementing auto-refresh interceptors in Axios
- **Database Optimization** — Indexing strategy for job search performance
- **Docker** — Containerizing Django with PostgreSQL for portable development

---

## Slide 11: Thank You

**Links:**

- GitHub: github.com/eliaset/job-board-platform
- Live Frontend: job-board-platform-smoky.vercel.app
- Live API: job-board-api-mxzh.onrender.com
- Swagger Docs: job-board-api-mxzh.onrender.com/api/docs/

**Questions?**
