CREATE TABLE employees (
    emp_id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    hire_date TEXT
);

CREATE TABLE dayforce_jobs (
    dayforce_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dayforce_job_name TEXT NOT NULL,
    is_exempt BOOLEAN NOT NULL,
    hourly_level INTEGER CHECK (hourly_level IN (1, 2, 3) OR hourly_level IS NULL),
    manager_level INTEGER CHECK (manager_level IN (1, 4) OR manager_level IS NULL),
    reports_to INTEGER,
    FOREIGN KEY (reports_to) REFERENCES dayforce_jobs(dayforce_id)
);

CREATE TABLE posted_jobs (
    posted_name_id INTEGER PRIMARY KEY AUTOINCREMENT,
    dayforce_id INTEGER NOT NULL,
    posted_job_name TEXT NOT NULL,
    FOREIGN KEY (dayforce_id) REFERENCES dayforce_jobs(dayforce_id)
);

CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name TEXT NOT NULL UNIQUE
);

CREATE TABLE job_departments (
    dayforce_id INTEGER NOT NULL,
    department_id INTEGER NOT NULL,
    PRIMARY KEY (dayforce_id, department_id),
    FOREIGN KEY (dayforce_id) REFERENCES dayforce_jobs(dayforce_id),
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
);

CREATE TABLE posting_tracker (
    posting_id INTEGER PRIMARY KEY AUTOINCREMENT,
    posted_name_id INTEGER NOT NULL,
    open_date TEXT NOT NULL,
    first_contact_date TEXT,
    offer_date TEXT,
    close_date TEXT,
    orientation_date TEXT,
    start_date TEXT,
    term_date TEXT DEFAULT NULL,
    is_replacement BOOLEAN NOT NULL DEFAULT FALSE,
    replacing_whom INTEGER,
    opened_by INTEGER,
    filled_by INTEGER,
    new_hire INTEGER,
    FOREIGN KEY (posted_name_id) REFERENCES posted_jobs(posted_name_id),
    FOREIGN KEY (replacing_whom) REFERENCES employees(emp_id),
    FOREIGN KEY (opened_by) REFERENCES employees(emp_id),
    FOREIGN KEY (filled_by) REFERENCES employees(emp_id),
    FOREIGN KEY (new_hire) REFERENCES employees(emp_id)
);

CREATE TABLE posting_metrics (
    metric_id INTEGER PRIMARY KEY AUTOINCREMENT,
    posting_id INTEGER NOT NULL,
    applicant_total INTEGER DEFAULT 0,
    applicants_called INTEGER DEFAULT 0,
    applicants_interviewed INTEGER DEFAULT 0,
    recorded_date TEXT NOT NULL,
    FOREIGN KEY (posting_id) REFERENCES posting_tracker(posting_id)
);

CREATE TABLE sources (
    source_id INTEGER PRIMARY KEY AUTOINCREMENT,
    posting_id INTEGER NOT NULL,
    source_name TEXT NOT NULL,                  -- Free-text: 'Indeed', 'LinkedIn', 'Other', etc.
    source_details TEXT,                        -- Optional details (e.g., for 'Other')
    referral_emp_id INTEGER,                    -- Required if source_name = 'Referral', NULL otherwise
    FOREIGN KEY (posting_id) REFERENCES posting_tracker(posting_id),
    FOREIGN KEY (referral_emp_id) REFERENCES employees(emp_id)
);