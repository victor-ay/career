import subprocess

def run_linkedin_scrap_process():
    subprocess.run(['DJANGO_SETTINGS_MODULE=career_proj.prod_settings python3','src/career/jobs_scrappers/linkedin_scrapper/get_linkedin_jobs_to_db.py'])