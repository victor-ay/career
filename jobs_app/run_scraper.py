import subprocess

def run_linkedin_scrap_process():
    subprocess.run(['python3','jobs_scrappers/linkedin_scrapper/get_linkedin_jobs_to_db.py'])