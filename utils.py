import spacy  # spaCy is used for advanced NLP tasks
import re     # Regex is used to extract patterns like years of experience

# Load the small English NLP model
nlp = spacy.load("en_core_web_sm")

# Predefined keywords to extract from resume/job description
# These can be expanded based on domain needs

# Technical & soft skills
SKILLS = [
    "python", "java", "c++", "c", "javascript", "typescript", "html", "css", "php",
    "sql", "mysql", "postgresql", "mongodb", "oracle", "machine learning", "deep learning", "nlp",
    "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly",
    "tensorflow", "keras", "pytorch", "scikit-learn", "mlflow",
    "flask", "django", "fastapi", "spring", "express", "node.js",
    "aws", "azure", "gcp", "docker", "kubernetes", "linux", "networking", "git", "ci/cd", "jenkins",
    "agile", "scrum", "jira", "project management", "communication", "teamwork",
    "problem solving", "leadership", "time management", "adaptability", "critical thinking"
]

JOB_TITLES = [
    "data scientist", "data analyst", "machine learning engineer",
    "software developer", "software engineer", "backend developer", "frontend developer",
    "full stack developer", "web developer", "cloud engineer", "devops engineer",
    "cybersecurity analyst", "security engineer", "business analyst", "product manager",
    "project manager", "database administrator", "network engineer", 
    "test engineer", "automation tester", "intern", "trainee", "technical lead", "solution architect"
]

EDUCATION_KEYWORDS = [
    "bca", "mca", "b.tech", "m.tech",  "bachelor", "master",
    "bsc", "msc", "phd", "mba", "computer science",
    "information technology", "electronics", "mechanical", "civil", "engineering",
    "science", "arts", "commerce", "statistics", "mathematics", "ai", "ml", "data science"
]

LANGUAGES = [
    "english", "hindi", "french", "german", "spanish", "tamil", "telugu", "marathi", "punjabi",
    "bengali", "gujarati", "malayalam", "kannada", "urdu", "japanese", "chinese", "korean", "russian", "portuguese"
]


# Function: extract_skills
# Extracts matching skills using spaCy tokenization and string matching

def extract_skills(text):
    """Extract matching skills from text using spaCy"""
    doc = nlp(text.lower())
    found_skills = set()

    # Match single tokens like "python"
    for token in doc:
        if token.text in SKILLS:
            found_skills.add(token.text)

    # Also check for multi-word skills like "machine learning"
    for skill in SKILLS:
        if skill in text.lower():
            found_skills.add(skill)

    return list(found_skills)


# Function: extract_fields
# Extracts fields such as skills, job titles, education, experience, languages

def extract_fields(text):
    """Extract skills, job title, education, experience, and languages from text"""
    text_lower = text.lower()
    doc = nlp(text_lower)

    # Extract skills from text using spaCy and predefined SKILLS list
    skills = extract_skills(text)

    # Extract job titles
    found_titles = [title for title in JOB_TITLES if title in text_lower]

    # Extract education keywords
    found_education = [edu for edu in EDUCATION_KEYWORDS if edu in text_lower]

    # Use regex to extract patterns like "2 years", "5+ yrs", "3yrs"
    experience_matches = re.findall(r'(\d+)\s*(?:\+?\s*)?(?:years?|yrs?)', text_lower)
    experience = [f"{exp} years" for exp in experience_matches]

    # Match known languages
    found_languages = [lang for lang in LANGUAGES if lang in text_lower]

    return {
        "skills": skills,
        "job_titles": found_titles,
        "education": found_education,
        "experience": experience,
        "languages": found_languages
    }


# SQLite DB: Insert analysis result into 'Result' table
# Called for each resume after it is analyzed

import sqlite3
from datetime import datetime

def insert_result(resume_id, job_id, score, matched_skills, matched_title, matched_education, matched_experience, matched_languages):
    """Insert a resume-job analysis result into the database"""
    conn = sqlite3.connect('instance/database.db')
    cursor = conn.cursor()

    cursor.execute('''
        INSERT INTO Result (
            resume_id,
            job_id,
            score,
            matched_skills,
            matched_title,
            matched_education,
            matched_experience,
            matched_languages,
            analysis_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        resume_id,
        job_id,
        score,
        ', '.join(matched_skills),
        ', '.join(matched_title),
        ', '.join(matched_education),
        ', '.join(matched_experience),
        ', '.join(matched_languages),
        datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    ))

    conn.commit()
    conn.close()


