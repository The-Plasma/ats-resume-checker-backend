# This file provides utility functions, including fetching job descriptions

def get_job_description(job_profile):
    """Return a sample job description based on the job profile."""
    # Predefined sample job descriptions (you can modify or expand this as needed)
    job_descriptions = {
        'software engineer': """
            We are looking for a Software Engineer to develop and maintain software applications.
            Responsibilities include writing clean, scalable code, testing and deploying programs, and collaborating with cross-functional teams.
            Required skills: Python, JavaScript, REST APIs, Git, Agile methodology.
        """,
        'data scientist': """
            We are seeking a Data Scientist to analyze large datasets and build predictive models.
            Responsibilities include data cleaning, building machine learning models, and communicating findings.
            Required skills: Python, R, Machine Learning, SQL, Data Visualization, Deep Learning.
        """,
        'project manager': """
            We are hiring a Project Manager to lead project teams, manage resources, and deliver results on time.
            Responsibilities include developing project plans, coordinating team efforts, and ensuring milestones are met.
            Required skills: Project Management, Agile, Communication, Risk Management, Budgeting.
        """
    }

    # Return the job description or a default if not found
    return job_descriptions.get(job_profile.lower(), "No job description found for this profile.")
