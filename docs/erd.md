# Job Board Platform - Entity Relationship Diagram

```mermaid
erDiagram
    User ||--o{ JobPosting : "posts"
    User ||--o{ JobApplication : "applies"
    User ||--o{ SavedJob : "saves"
    JobCategory ||--o{ JobPosting : "categorizes"
    JobPosting ||--o{ JobApplication : "receives"
    JobPosting ||--o{ SavedJob : "is_saved_in"

    User {
        int id PK
        string email UK "Unique"
        string password
        string first_name
        string last_name
        string role "admin, employer, job_seeker"
        string company_name "nullable"
        string bio "nullable"
        string phone "nullable"
        datetime date_joined
    }

    JobCategory {
        int id PK
        string name UK "Unique"
        text description "nullable"
        datetime created_at
    }

    JobPosting {
        int id PK
        string title
        text description
        int company_id FK
        int category_id FK
        string location
        string job_type "full_time, part_time, etc."
        decimal salary_min "nullable"
        decimal salary_max "nullable"
        text requirements
        boolean is_active
        datetime created_at
        datetime updated_at
    }

    JobApplication {
        int id PK
        int job_id FK
        int applicant_id FK
        text cover_letter
        string status "pending, reviewed, accepted, rejected"
        datetime applied_at
        datetime updated_at
    }

    SavedJob {
        int id PK
        int user_id FK
        int job_id FK
        datetime saved_at
    }
```

## Relationships

1. **User 1:N JobPosting**
   - An Employer (User) can post multiple Jobs.
   - A Job belongs to one Employer.

2. **JobCategory 1:N JobPosting**
   - A Category can have multiple Jobs.
   - A Job belongs to one Category.

3. **User 1:N JobApplication**
   - A Job Seeker (User) can submit multiple Applications.
   - An Application belongs to one Applicant.

4. **JobPosting 1:N JobApplication**
   - A Job can receive multiple Applications.
   - An Application belongs to one Job.

5. **User 1:N SavedJob** (Many-to-Many via Join Table)
   - A User can save multiple Jobs.
   - A Job can be saved by multiple Users.
