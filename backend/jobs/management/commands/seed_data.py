"""
Management command to seed demo data (categories + sample jobs).
"""

from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from jobs.models import JobCategory, JobPosting

User = get_user_model()

CATEGORIES = [
    (
        "Software Engineering",
        "Software development, web, mobile, and backend engineering roles.",
    ),
    (
        "Data Science",
        "Data analysis, machine learning, and AI positions.",
    ),
    (
        "Design",
        "UI/UX design, graphic design, and creative roles.",
    ),
    (
        "Marketing",
        "Digital marketing, SEO, content, and growth roles.",
    ),
    (
        "DevOps & Cloud",
        "Infrastructure, CI/CD, cloud engineering positions.",
    ),
    (
        "Product Management",
        "Product strategy, roadmapping, and execution roles.",
    ),
]

JOBS = [
    {
        "title": "Senior Backend Engineer",
        "description": (
            "We are looking for a Senior Backend Engineer to design and "
            "build scalable APIs using Django and PostgreSQL. You will work "
            "with a cross-functional team to deliver reliable microservices.\n\n"
            "Responsibilities:\n"
            "- Design and implement RESTful APIs\n"
            "- Optimize database queries for performance\n"
            "- Write comprehensive unit and integration tests\n"
            "- Participate in code reviews and architectural decisions"
        ),
        "category_name": "Software Engineering",
        "location": "Addis Ababa, Ethiopia",
        "job_type": "full_time",
        "salary_min": 80000,
        "salary_max": 120000,
        "requirements": (
            "- 4+ years Python/Django experience\n"
            "- Strong PostgreSQL knowledge\n"
            "- Experience with REST API design\n"
            "- Familiarity with Docker and CI/CD\n"
            "- Excellent problem-solving skills"
        ),
    },
    {
        "title": "Frontend React Developer",
        "description": (
            "Join our team as a Frontend Developer building modern web applications "
            "with React, TypeScript, and Tailwind CSS.\n\n"
            "Responsibilities:\n"
            "- Build responsive and accessible user interfaces\n"
            "- Integrate with REST APIs\n"
            "- Write clean, maintainable component code\n"
            "- Collaborate with designers and backend engineers"
        ),
        "category_name": "Software Engineering",
        "location": "Remote",
        "job_type": "remote",
        "salary_min": 60000,
        "salary_max": 95000,
        "requirements": (
            "- 2+ years React experience\n"
            "- Strong JavaScript/TypeScript skills\n"
            "- Experience with state management\n"
            "- Knowledge of responsive design"
        ),
    },
    {
        "title": "Data Scientist",
        "description": (
            "We need a Data Scientist to analyze large datasets, build predictive models, "
            "and drive data-informed decisions across the organization.\n\n"
            "Responsibilities:\n"
            "- Develop and deploy ML models\n"
            "- Analyze business data and present insights\n"
            "- Build data pipelines\n"
            "- Collaborate with engineering teams"
        ),
        "category_name": "Data Science",
        "location": "Nairobi, Kenya",
        "job_type": "full_time",
        "salary_min": 70000,
        "salary_max": 110000,
        "requirements": (
            "- MSc in CS, Statistics, or related field\n"
            "- Proficiency in Python, pandas, scikit-learn\n"
            "- Experience with SQL and data visualization\n"
            "- Strong communication skills"
        ),
    },
    {
        "title": "UI/UX Designer",
        "description": (
            "We are looking for a talented UI/UX Designer to create intuitive and "
            "visually appealing interfaces for our web and mobile products.\n\n"
            "Responsibilities:\n"
            "- Create wireframes, prototypes, and high-fidelity mockups\n"
            "- Conduct user research and usability testing\n"
            "- Develop and maintain design systems\n"
            "- Work closely with product and engineering teams"
        ),
        "category_name": "Design",
        "location": "Lagos, Nigeria",
        "job_type": "full_time",
        "salary_min": 45000,
        "salary_max": 75000,
        "requirements": (
            "- 3+ years UI/UX experience\n"
            "- Proficiency in Figma or Sketch\n"
            "- Portfolio demonstrating strong visual design skills\n"
            "- Understanding of accessibility standards"
        ),
    },
    {
        "title": "DevOps Engineer (Part-Time)",
        "description": (
            "Part-time DevOps Engineer to help us build and maintain CI/CD pipelines, "
            "manage cloud infrastructure, and improve system reliability.\n\n"
            "Responsibilities:\n"
            "- Manage AWS/GCP infrastructure\n"
            "- Build and maintain CI/CD pipelines\n"
            "- Monitor system health and respond to incidents\n"
            "- Automate deployment processes"
        ),
        "category_name": "DevOps & Cloud",
        "location": "Remote",
        "job_type": "part_time",
        "salary_min": 40000,
        "salary_max": 60000,
        "requirements": (
            "- Experience with AWS or GCP\n"
            "- Knowledge of Docker and Kubernetes\n"
            "- Familiarity with GitHub Actions or Jenkins\n"
            "- Strong Linux skills"
        ),
    },
    {
        "title": "Digital Marketing Intern",
        "description": (
            "Exciting internship opportunity in digital marketing! Learn SEO, "
            "content marketing, social media strategy, and analytics while working "
            "with an experienced team.\n\n"
            "Responsibilities:\n"
            "- Assist with social media campaigns\n"
            "- Write blog posts and marketing copy\n"
            "- Analyze campaign performance\n"
            "- Support email marketing efforts"
        ),
        "category_name": "Marketing",
        "location": "Addis Ababa, Ethiopia",
        "job_type": "internship",
        "salary_min": 5000,
        "salary_max": 10000,
        "requirements": (
            "- Currently pursuing a marketing or communications degree\n"
            "- Strong writing skills\n"
            "- Familiarity with social media platforms\n"
            "- Eagerness to learn"
        ),
    },
    {
        "title": "Product Manager",
        "description": (
            "We need a Product Manager to drive product strategy and roadmap for "
            "our SaaS platform. You will work closely with engineering, "
            "design, and business teams.\n\n"
            "Responsibilities:\n"
            "- Define product vision and roadmap\n"
            "- Prioritize features based on user needs and business impact\n"
            "- Write detailed product requirements\n"
            "- Analyze metrics and iterate on the product"
        ),
        "category_name": "Product Management",
        "location": "Nairobi, Kenya",
        "job_type": "contract",
        "salary_min": 65000,
        "salary_max": 100000,
        "requirements": (
            "- 3+ years product management experience\n"
            "- Experience with agile methodologies\n"
            "- Strong analytical and communication skills\n"
            "- Technical background preferred"
        ),
    },
    {
        "title": "Full Stack Developer",
        "description": (
            "Full Stack Developer to build end-to-end features for our job board "
            "platform using Django and React.\n\n"
            "Responsibilities:\n"
            "- Develop frontend and backend features\n"
            "- Design database schemas\n"
            "- Write API documentation\n"
            "- Deploy to cloud platforms"
        ),
        "category_name": "Software Engineering",
        "location": "Addis Ababa, Ethiopia",
        "job_type": "full_time",
        "salary_min": 55000,
        "salary_max": 85000,
        "requirements": (
            "- Experience with Django and React\n"
            "- Knowledge of PostgreSQL\n"
            "- Familiarity with Git and CI/CD\n"
            "- Strong problem-solving skills"
        ),
    },
]


class Command(BaseCommand):
    help = "Seed the database with demo categories and job postings."

    def handle(self, *args, **options):
        # Create or get employer for demo jobs
        employer, created = User.objects.get_or_create(
            email="employer@jobboard.com",
            defaults={
                "first_name": "Demo",
                "last_name": "Employer",
                "role": "employer",
                "company_name": "TechCorp Africa",
            },
        )
        if created:
            employer.set_password("Employer@123")
            employer.save()
            self.stdout.write(self.style.SUCCESS("Created demo employer: employer@jobboard.com / Employer@123"))

        # Seed categories
        cat_map = {}
        for name, desc in CATEGORIES:
            cat, created = JobCategory.objects.get_or_create(
                name=name, defaults={"description": desc}
            )
            cat_map[name] = cat
            if created:
                self.stdout.write(f"  + Category: {name}")

        # Seed jobs
        for job_data in JOBS:
            cat_name = job_data.pop("category_name")
            title = job_data["title"]
            if not JobPosting.objects.filter(title=title, company=employer).exists():
                JobPosting.objects.create(
                    company=employer,
                    category=cat_map.get(cat_name),
                    **job_data,
                )
                self.stdout.write(f"  + Job: {title}")

        self.stdout.write(self.style.SUCCESS(f"\nSeeded {len(CATEGORIES)} categories and {len(JOBS)} jobs."))
