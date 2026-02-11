# Job Board Platform — Demo Video Script

> **Total Duration:** ~4-5 minutes. Record with screen capture (OBS, Loom, or similar).

---

## Intro (0:00 – 0:30)

**Show:** The frontend homepage loaded with job listings.

**Say:**

> "Hi, I'm Elias. This is my Project Nexus submission — a full-stack Job Board Platform built with Django REST Framework and React. The platform supports three roles: Admin, Employer, and Job Seeker, with JWT authentication, advanced filtering, and a fully documented REST API. Let me walk you through it."

---

## 1. API Documentation (0:30 – 1:00)

**Show:** Navigate to `https://job-board-api-mxzh.onrender.com/api/docs/`

**Say:**

> "First, here's the Swagger documentation. Every endpoint is documented with request/response schemas. We have Auth endpoints for registration and login, Jobs endpoints with full CRUD, Applications for applying and tracking, and Saved Jobs for bookmarking. All of this is auto-generated from the code using drf-spectacular."

**Do:** Expand one or two endpoints to show the request body and response schema.

---

## 2. Browse Jobs (1:00 – 1:30)

**Show:** Go to the frontend homepage.

**Say:**

> "The homepage shows all available jobs. Users can search by keyword, filter by category, job type, and sort by date or salary. The data comes from the paginated REST API. Let me filter by 'Software Engineering' category..."

**Do:** Use the category filter, then search for "backend". Show the results updating.

---

## 3. Register & Login (1:30 – 2:15)

**Show:** Click "Register" in the navbar.

**Say:**

> "Let me register a new job seeker account. I'll fill in the details — notice the role selector. When I choose 'Employer', a company name field appears. For now, I'll register as a Job Seeker."

**Do:** Fill the form and submit. Show the auto-login redirect to the dashboard.

> "After registration, the backend returns JWT tokens and the user is automatically logged in. No separate login step needed."

---

## 4. Apply for a Job (2:15 – 2:45)

**Show:** Click on a job posting from the homepage.

**Say:**

> "Here's a job detail page. It shows the full description, requirements, salary range, and company info. As a job seeker, I can apply with a cover letter."

**Do:** Write a brief cover letter and click Apply. Show the success message.

> "The application is tracked with status — Pending, Reviewed, Accepted, or Rejected. A unique constraint prevents applying to the same job twice."

---

## 5. Job Seeker Dashboard (2:45 – 3:00)

**Show:** Navigate to Dashboard.

**Say:**

> "My dashboard shows all my applications with their current status. Job seekers can track where they've applied and see updates from employers."

---

## 6. Employer Features (3:00 – 3:45)

**Show:** Log out, then log in as the demo employer (`employer@jobboard.com` / `Employer@123`).

**Say:**

> "Now let me switch to an employer account. Employers can post new jobs—"

**Do:** Click "Post Job", fill in a job title, description, category, and salary range. Submit.

> "The employer dashboard shows all posted jobs with their application counts. Employers can review applications and update their status — accept, reject, or mark as reviewed."

**Do:** Show the dashboard with job listings and application management.

---

## 7. Best Practices & DevOps (3:45 – 4:15)

**Show:** Switch to GitHub repo page.

**Say:**

> "For best practices: the project uses Docker for containerized deployment, GitHub Actions for CI/CD which runs linting and all 27 unit tests on every push, API rate limiting for security, database indexing for performance, and comprehensive API documentation. The backend is deployed on Render with PostgreSQL, and the frontend on Vercel."

**Do:** Show the GitHub Actions CI passing (green checkmark).

---

## 8. Closing (4:15 – 4:30)

**Show:** Go back to the frontend homepage.

**Say:**

> "To summarize — this Job Board Platform demonstrates full-stack development with Django REST Framework, role-based authentication, database optimization, containerization, CI/CD, and cloud deployment. All the code is on GitHub, and the live demo is accessible at the links in the README. Thank you for watching!"

---

## Tips for Recording

1. **Use a clean browser** — no extra tabs or bookmarks visible
2. **Zoom in** to 125% so text is readable on screen
3. **Keep a steady pace** — don't rush through features
4. **Test everything beforehand** — make sure all endpoints work
5. **Upload to YouTube** (unlisted) or Google Drive with sharing enabled
