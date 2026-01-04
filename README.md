# AI-Powered Resume Analyzer

An AI-powered web application that automates resume screening by analyzing and matching candidate resumes with a given job description using Natural Language Processing (NLP) techniques.

This project is designed to help recruiters reduce manual effort by extracting key information from resumes and ranking candidates based on their relevance to a job description.

## Features

- Upload resumes in PDF format
- Input job description in text or paragraph format
- Automatic extraction of:
  - Skills
  - Job Title
  - Education
  - Experience
  - Languages
- Resume-to-job matching using NLP techniques
- Resume ranking based on similarity score
- Downloadable analysis report
- Stores resume analysis records in a database
- Clean and easy-to-use web interface

## NLP Techniques Used

- Text preprocessing and normalization
- Keyword extraction using spaCy
- TF-IDF vectorization
- Cosine similarity for resume-to-job matching
- Field-level similarity comparison

## Workflow Overview

1. User uploads one or more resumes
2. User enters the job description
3. Flask backend processes uploaded resume files
4. NLP engine extracts required information from resumes
5. Extracted resume data is compared with the job description
6. Similarity scores are calculated for each resume
7. Results are stored in the database
8. Ranked resumes are displayed on the results page

## Tech Stack

- Frontend: HTML, CSS, Bootstrap
- Backend: Python, Flask
- NLP: spaCy, TF-IDF, Cosine Similarity
- Database: SQLite
- File Processing: PDF parsing
- Libraries: pandas, scikit-learn

## Project Structure

AI-Resume-Analyzer/
├── app.py
├── utils.py
├── requirements.txt
├── README.md
├── database.db
├── static/
│   └── style.css
└── templates/
    ├── index.html
    └── result.html

## Setup & Run

1. Clone the repository  
git clone https://github.com/<Manasvi154>/AI-Resume-Analyzer.git  

2. Navigate to the project directory  
cd AI-Resume-Analyzer  

3. Create a virtual environment  
python -m venv venv  

4. Activate the virtual environment  
venv\Scripts\activate  

5. Install dependencies  
pip install -r requirements.txt  

6. Run the application  
python app.py  

Open the application in browser at:  
http://localhost:5000

## Database Details

The application uses SQLite to store resume analysis records including:
- Resume file name
- Matching score
- Matched skills
- Extracted fields
- Analysis date

## Best Practices Followed

- Modular and readable code structure
- Separation of frontend, backend, and NLP logic
- NLP-based resume matching instead of basic keyword search
- Persistent data storage using SQLite
- Scalable design for future improvements

## Future Enhancements

- Cloud deployment using AWS
- Support for DOCX resumes
- Machine learning-based resume ranking
- User authentication and role-based access
- Advanced analytics dashboard for recruiters

## Author

Manasvi Pawar  
Cloud & Data Enthusiast
