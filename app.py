from flask import Flask, request, jsonify
from pymongo import MongoClient
from models import analyze_resume
import os
import PyPDF2

app = Flask(__name__)

# Connect to MongoDB
client = MongoClient("mongodb+srv://test:Test25@cluster0.pjsuo.mongodb.net/")
db = client['ats_db']
resume_collection = db['resumes']

def extract_text_from_pdf(pdf_file):
    """Extract text from a PDF file using PyPDF2."""
    reader = PyPDF2.PdfReader(pdf_file)
    text = ''
    for page in reader.pages:
        text += page.extract_text()
    return text

@app.route('/upload_resume', methods=['POST'])
def upload_resume():
    file = request.files.get('file')
    job_profile = request.form.get('job_profile')  # Job profile passed in the form data
    
    if not file or not job_profile:
        return jsonify({'error': 'File and job profile are required'}), 400
    
    # Check file type (simple validation based on filename extension)
    filename = file.filename.lower()
    
    if filename.endswith('.pdf'):
        # Extract text from the PDF file
        try:
            resume_text = extract_text_from_pdf(file)
            if not resume_text.strip():
                return jsonify({'error': 'Unable to extract text from PDF.'}), 400
        except Exception as e:
            return jsonify({'error': f'Error processing PDF: {str(e)}'}), 500
    else:
        # Handle other text files (assuming they are plain text or similar)
        try:
            resume_text = file.read().decode('utf-8')
        except UnicodeDecodeError:
            return jsonify({'error': 'Failed to decode file. Please upload a valid UTF-8 encoded text file.'}), 400

    # Analyze the resume using the ML model and the provided job profile
    ats_score, feedback = analyze_resume(resume_text, job_profile)

    # Store the resume and results in MongoDB
    resume_data = {
        'filename': file.filename,
        'content': resume_text,
        'ats_score': ats_score,
        'feedback': feedback,
        'job_profile': job_profile
    }
    result = resume_collection.insert_one(resume_data)

    return jsonify({
        'message': 'Resume uploaded and analyzed successfully!',
        'ats_score': ats_score,
        'feedback': feedback,
        'resume_text': resume_text,  # Return the extracted text
        'resume_id': str(result.inserted_id)
    }), 201

@app.route('/resume/<resume_id>', methods=['GET'])
def get_resume(resume_id):
    resume = resume_collection.find_one({'_id': resume_id})
    if not resume:
        return jsonify({'error': 'Resume not found'}), 404

    return jsonify({
        'filename': resume['filename'],
        'ats_score': resume['ats_score'],
        'feedback': resume['feedback'],
        'content': resume['content'],
        'job_profile': resume['job_profile']
    })

@app.route('/hello', methods=['GET'])
def hello_world():
    return jsonify({'message': 'Hello, World!'}), 200


if __name__ == '__main__':
    app.run(debug=True)
