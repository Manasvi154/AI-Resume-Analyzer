# -- Imports --
from flask import Flask, render_template, request, send_from_directory, flash, redirect, url_for, make_response
import os
import sqlite3  # For SQLite database interaction
import PyPDF2  # For extracting text from PDF files
import numpy as np # for numerical computations in python
import csv
import io  # For in-memory file handling
import sklearn
from datetime import datetime  # To add timestamps
from sklearn.feature_extraction.text import TfidfVectorizer  # Converts text to numerical feature vectors
from sklearn.metrics.pairwise import cosine_similarity  # To compare similarity between vectors
from utils import extract_fields, insert_result  # Custom utility functions (skills/fields extraction, DB insert)
from werkzeug.utils import secure_filename  # Safely handles uploaded filenames

# ----Flask App Setup --
app = Flask(__name__)
app.secret_key = "supersecretkey"  # Secret key to manage sessions and flashing messages

UPLOAD_FOLDER = "uploads"  # Folder to store uploaded resume files
DATABASE = "instance/database.db"  # SQLite database file
SIMILARITY_THRESHOLD = 50.0  # Default threshold to indicate a "match"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Create required folders if not exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("instance", exist_ok=True)

# --- Helper Function: Extract text from PDF --
def extract_text_from_pdf(pdf_path):
    """Reads and extracts text from the uploaded PDF file"""
    text = ""
    with open(pdf_path, "rb") as f:
        reader = PyPDF2.PdfReader(f)
        for page in reader.pages:
            text += page.extract_text() or ""
    return text

# --- Database: Job Description ---
def insert_or_get_job_id(content):
    """Checks if the job description exists in DB, else inserts it"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    cursor.execute("SELECT id FROM JobDescription WHERE content = ?", (content,))
    result = cursor.fetchone()

    if result:
        job_id = result[0]
    else:
        upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute("INSERT INTO JobDescription (content, upload_date) VALUES (?, ?)", (content, upload_date))
        conn.commit()
        job_id = cursor.lastrowid

    conn.close()
    return job_id

# --- Database: Resume ---
def insert_resume(filename):
    """Inserts uploaded resume record into database"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    upload_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("INSERT INTO Resume (filename, upload_date) VALUES (?, ?)", (filename, upload_date))
    conn.commit()
    resume_id = cursor.lastrowid
    conn.close()
    return resume_id

# --- Database: Result ---
def save_result(resume_id, job_id, score, fields):
    """Stores resume analysis results in the database"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    analysis_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute('''
        INSERT INTO Result (
            resume_id, job_id, score, matched_skills, 
            matched_title, matched_education, matched_experience, matched_languages, analysis_date
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (
        resume_id,
        job_id,
        score,
        ", ".join(fields["skills"]),
        ", ".join(fields["job_titles"]),
        ", ".join(fields["education"]),
        ", ".join(fields["experience"]),
        ", ".join(fields["languages"]),
        analysis_date
    ))
    conn.commit()
    conn.close()

# --- Analysis: Match Fields and Score ---
def analyze_resumes(job_desc, resumes_dict):
    """
    Main logic for analyzing resumes:
    - Extract fields from JD and resumes
    - Vectorize for TF-IDF
    - Use cosine similarity to calculate score
    """
    job_fields = extract_fields(job_desc)
    job_text = " ".join(
        job_fields["skills"] + job_fields["job_titles"] +
        job_fields["education"] + job_fields["experience"] +
        job_fields["languages"]
    )
    if not job_text.strip():
        job_text = "empty"

    texts = [job_text]
    results = []

    for filename, content in resumes_dict.items():
        resume_fields = extract_fields(content)
        resume_text = " ".join(
            resume_fields["skills"] + resume_fields["job_titles"] +
            resume_fields["education"] + resume_fields["experience"] +
            resume_fields["languages"]
        )
        if not resume_text.strip():
            resume_text = "empty"
        texts.append(resume_text)

        results.append({
            "filename": filename,
            "fields": resume_fields
        })

    # TF-IDF Vectorization + Cosine Similarity
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(texts)
    similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

    for i in range(len(results)):
        results[i]["score"] = round(similarity_scores[i] * 100, 2)

    results.sort(key=lambda x: x["score"], reverse=True)
    return results

# --- Home Route ---
@app.route("/", methods=["GET", "POST"])
def index():
    """
    Main page route:
    - Handles resume and JD upload
    - Performs analysis
    - Stores results in DB
    - Displays ranked resumes
    """
    results = []

    if request.method == "POST":
        job_desc = request.form.get("job_description")
        files = request.files.getlist("resumes")

        if not job_desc:
            flash("Job description is required!", "error")
            return redirect(url_for("index"))

        if not files:
            flash("Please upload at least one PDF resume.", "error")
            return redirect(url_for("index"))

        resumes_dict = {}
        file_resume_ids = {}

        for file in files:
            if not file.filename.endswith(".pdf"):
                flash(f"{file.filename} is not a PDF file.", "error")
                return redirect(url_for("index"))

            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            file.save(file_path)

            text = extract_text_from_pdf(file_path)
            resumes_dict[filename] = text
            resume_id = insert_resume(filename)
            file_resume_ids[filename] = resume_id

        if resumes_dict:
            job_id = insert_or_get_job_id(job_desc)
            job_fields = extract_fields(job_desc)
            analyzed_results = analyze_resumes(job_desc, resumes_dict)

            for res in analyzed_results:
                filename = res["filename"]
                score = res["score"]
                resume_id = file_resume_ids[filename]
                resume_fields = res["fields"]

                # Match fields
                matched_skills = list(set(job_fields["skills"]) & set(resume_fields["skills"]))
                matched_title = list(set(job_fields["job_titles"]) & set(resume_fields["job_titles"]))
                matched_education = list(set(job_fields["education"]) & set(resume_fields["education"]))
                matched_experience = list(set(job_fields["experience"]) & set(resume_fields["experience"]))
                matched_languages = list(set(job_fields["languages"]) & set(resume_fields["languages"]))

                insert_result(
                    resume_id=resume_id,
                    job_id=job_id,
                    score=score,
                    matched_skills=matched_skills,
                    matched_title=matched_title,
                    matched_education=matched_education,
                    matched_experience=matched_experience,
                    matched_languages=matched_languages
                )

                res["fields"] = {
                    "skills": matched_skills,
                    "job_titles": matched_title,
                    "education": matched_education,
                    "experience": matched_experience,
                    "languages": matched_languages
                }

            results = analyzed_results

            if all(res["score"] == 0.0 for res in results):
                flash("No matching resumes found.", "info")

    return render_template("index.html", results=results, threshold=SIMILARITY_THRESHOLD)

# --- Resume Download Route ---
@app.route("/download/<filename>")
def download_resume(filename):
    """Allows recruiter to download resume from uploads folder"""
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename, as_attachment=True)

# --- CSV Report Download Route --
@app.route("/download_report", methods=["POST"])
def download_report():
    """Exports only the latest analysis result as CSV"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()

    # Get the most recent job_id from JobDescription table
    cursor.execute("SELECT id FROM JobDescription ORDER BY upload_date DESC LIMIT 1")
    latest_job = cursor.fetchone()

    if not latest_job:
        conn.close()
        flash("No analysis data available to export.", "error")
        return redirect(url_for("index"))

    latest_job_id = latest_job[0]

    # Fetch only the results related to the latest job_id
    cursor.execute('''
        SELECT Resume.filename, Result.score, Result.matched_skills,
               Result.matched_title, Result.matched_education, 
               Result.matched_experience, Result.matched_languages
        FROM Result
        JOIN Resume ON Result.resume_id = Resume.id
        WHERE Result.job_id = ?
        ORDER BY Result.score DESC
    ''', (latest_job_id,))
    rows = cursor.fetchall()
    conn.close()

    # Write to CSV
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["Filename", "Score (%)", "Matched Skills", "Matched Title", "Education", "Experience", "Languages"])
    writer.writerows(rows)

    response = make_response(output.getvalue())
    response.headers["Content-Disposition"] = "attachment; filename=resume_analysis_report.csv"
    response.headers["Content-Type"] = "text/csv"
    return response


# --- Run the App --
if __name__ == "__main__":
    app.run(debug=True)


