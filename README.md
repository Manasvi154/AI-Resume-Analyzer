# AI-Powered Resume Analyzer

An AI-powered web application that automates resume screening by analyzing and matching candidate resumes with job descriptions using Natural Language Processing (NLP) and Machine Learning techniques. The system extracts key information from resumes, calculates similarity scores, ranks candidates, and generates downloadable reports to simplify the recruitment process.

---

# Executive Summary

Recruiters often spend significant time manually reviewing hundreds of resumes for a single job opening. This project automates the initial screening process by comparing uploaded resumes with a job description using NLP techniques.
The application extracts important information such as skills, education, experience, job titles, and languages from resumes, calculates similarity scores using TF-IDF and Cosine Similarity, ranks candidates based on relevance, and stores the analysis results in an SQLite database. A recruiter can also download the complete analysis as a CSV report.

---

# Business Problem

Recruitment teams face several challenges during resume screening:

- Manual resume shortlisting is time-consuming.
- Large volumes of resumes increase recruiter workload.
- Different resume formats make comparison difficult.
- Qualified candidates may be overlooked.
- Traditional keyword-based filtering lacks contextual understanding.

This project addresses these challenges by providing an automated, accurate, and scalable resume screening solution.

---

# Methodology

The complete workflow of the application is as follows:

### Step 1 – Resume Upload
- Recruiter uploads one or more resumes in PDF format.
- Job description is entered through the web interface.

### Step 2 – Resume Processing
- PDF resumes are converted into plain text.
- Text preprocessing and cleaning are performed.

### Step 3 – Information Extraction
Using spaCy NLP, the system extracts:

- Technical Skills
- Soft Skills
- Job Titles
- Educational Qualifications
- Experience
- Languages

### Step 4 – Resume Matching

The extracted resume content is compared with the job description using:

- TF-IDF Vectorization
- Cosine Similarity

A similarity score is calculated for every resume.

### Step 5 – Candidate Ranking

Candidates are ranked automatically according to their similarity scores.

### Step 6 – Result Storage & Report Generation

The application:

- Stores analysis results in SQLite
- Displays ranked candidates
- Allows downloading the analysis as a CSV report

---

# Skills & Technologies

### Programming Languages

- Python
- HTML
- CSS
- JavaScript

### Frameworks

- Flask

### NLP & Machine Learning

- spaCy
- TF-IDF Vectorization
- Cosine Similarity
- Scikit-learn
- Random Forest Classifier

### Database

- SQLite

### Libraries

- Pandas
- NumPy
- PyPDF2
- Joblib
- Regex

### Development Tools

- VS Code
- Git
- GitHub

---

# Results & Business Recommendation

### Results

- Successfully extracted structured information from PDF resumes.
- Automatically matched resumes against job descriptions.
- Ranked candidates based on similarity scores.
- Generated downloadable CSV reports.
- Stored historical analysis records in SQLite.
- Machine Learning model achieved **83.33% classification accuracy** after introducing controlled label noise for better real-world generalization.
<img width="1887" height="1018" alt="Screenshot 2025-05-18 115709" src="https://github.com/user-attachments/assets/d46c69bf-3346-40de-8754-657e15dd64ea" />
<img width="1838" height="1012" alt="Screenshot 2025-05-18 115841" src="https://github.com/user-attachments/assets/70d52ad7-39ca-4f38-b9f9-241cf6f75c79" />


### Business Recommendations

- Reduce manual resume screening effort.
- Improve recruiter productivity.
- Shortlist candidates faster.
- Minimize human bias during initial screening.
- Standardize candidate evaluation using AI-driven analysis.

---

# Next Steps

Future improvements planned for the project include:

- Deploy the application on AWS Cloud.
- Support DOCX resume files.
- Improve resume parsing using transformer-based NLP models.
- Add recruiter authentication and role management.
- Integrate advanced analytics dashboards.
- Build REST APIs for ATS integration.
- Add email notifications for shortlisted candidates.
- Support multilingual resume analysis.



**Manasvi Pawar**

MCA (Artificial Intelligence & Machine Learning)

Python | NLP | Machine Learning | Flask | SQL | Data Analytics
