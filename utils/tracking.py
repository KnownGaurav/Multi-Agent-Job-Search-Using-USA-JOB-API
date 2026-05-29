import csv
import os
import datetime
import re

def save_cover_letter_file(job_title, cover_letter, directory="data/cover_letters"):
    """
    Sanitizes the job title and saves the generated cover letter as a text file.
    """
    # Remove leading/trailing spaces and replace unsafe filename characters
    clean_job_title = job_title.strip()
    clean_job_title = re.sub(r'[\\/*?:"<>|\s]+', "_", clean_job_title)
    
    # Ensure directory exists
    os.makedirs(directory, exist_ok=True)
    
    # Generate unique timestamped filename
    filename = f"{clean_job_title}_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
    filepath = os.path.join(directory, filename)
    
    # Added encoding="utf-8" to prevent crashes with LLM-generated special characters
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(cover_letter)
        
    return filepath

def log_application(job_title, agency, resume_summary, filepath="data/applications_log.csv"):
    """
    Logs the processed application detail into a CSV file.
    """
    # Securely extract and create the base directory path if it exists
    dir_name = os.path.dirname(filepath)
    if dir_name:
        os.makedirs(dir_name, exist_ok=True)
        
    exists = os.path.exists(filepath)
    
    with open(filepath, "a", newline='', encoding="utf-8") as csvfile:
        writer = csv.writer(csvfile)
        if not exists:
            writer.writerow(["Job Title", "Agency", "ResumeSummary", "DateApplied"])
        
        # Handle potential None or empty values gracefully with fallbacks
        safe_title = (job_title or "Unknown Title").strip()
        safe_agency = (agency or "Unknown Agency").strip()
        safe_summary = (resume_summary or "No Summary Provided").strip()
        
        writer.writerow([
            safe_title,
            safe_agency,
            safe_summary[:150], # Truncate snippet for clean csv rows
            datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        ])