import sqlite3
from datetime import datetime

conn = sqlite3.connect("instance/database.db")
cursor = conn.cursor()

# --- Resume Table ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS Resume (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    filename TEXT,
    upload_date TEXT
)
""")

# --- Job Description Table ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS JobDescription (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    content TEXT,
    upload_date TEXT
)
""")

# --- Result Table ---
cursor.execute("""
CREATE TABLE IF NOT EXISTS Result (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    resume_id INTEGER,
    job_id INTEGER,
    score REAL,
    matched_skills TEXT,
    matched_title TEXT,
    matched_education TEXT,
    matched_experience TEXT,
    matched_languages TEXT,
    analysis_date TEXT,
    FOREIGN KEY (resume_id) REFERENCES Resume(id),
    FOREIGN KEY (job_id) REFERENCES JobDescription(id)
)
""")

conn.commit()
conn.close()
print("✅ Database created successfully.")
print("✅ Tables created successfully!")


