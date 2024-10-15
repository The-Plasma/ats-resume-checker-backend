import spacy
from sklearn.feature_extraction.text import TfidfVectorizer
from utils import get_job_description  # Assume you have a function that gets the job description

# Load the spaCy model for NLP
nlp = spacy.load('en_core_web_sm')

# Define a list of common sections in a resume
EXPECTED_SECTIONS = ['experience', 'education', 'skills', 'projects', 'certifications']

# Define important action words typically seen in resumes
ACTION_WORDS = ['managed', 'developed', 'designed', 'led', 'implemented', 'created', 'optimized']

def analyze_resume(resume_text, job_profile):
    # Tokenize and process the resume text using spaCy
    resume_doc = nlp(resume_text)
    
    # Get the job description based on the job profile
    job_description = get_job_description(job_profile)

    # Use TF-IDF to analyze similarity between resume and job description
    vectorizer = TfidfVectorizer()
    texts = [resume_text, job_description]
    tfidf_matrix = vectorizer.fit_transform(texts)
    
    # Get the similarity score between resume and job description
    ats_score = (tfidf_matrix[0] * tfidf_matrix[1].T).toarray()[0][0] * 100
    
    # Provide detailed feedback
    feedback = []

    # Check length of the resume
    if len(resume_doc) < 200:
        feedback.append("Your resume is too short. Consider adding more details to showcase your qualifications.")

    # Check for missing key sections like 'experience', 'education', etc.
    missing_sections = [section for section in EXPECTED_SECTIONS if section not in resume_text.lower()]
    if missing_sections:
        feedback.append(f"Your resume is missing the following sections: {', '.join(missing_sections)}. Consider adding them.")

    # Check for action words that indicate strong achievement-oriented language
    action_words_found = any(word in resume_text.lower() for word in ACTION_WORDS)
    if not action_words_found:
        feedback.append("Your resume could benefit from more action words like 'developed', 'led', 'managed' to highlight your achievements.")

    # Check for keyword match with job description (based on TF-IDF)
    if ats_score < 50:
        feedback.append("Your resume has a low match with the job description. Consider tailoring it to include relevant keywords.")

    # Check for overall structure (simple heuristic based on basic grammar)
    if len([sent for sent in resume_doc.sents if len(sent.text.split()) > 15]) < 3:
        feedback.append("Some sentences are too short. Consider adding more depth to your experiences and achievements.")

    # Provide overall summary
    if not feedback:
        feedback.append("Your resume looks well-structured and relevant to the job description.")

    return round(ats_score, 2), feedback
