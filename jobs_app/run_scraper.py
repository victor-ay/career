import subprocess

# def run_linkedin_scrap_process():
#     subprocess.run(['python3','src/career/jobs_scrappers/linkedin_scrapper/get_linkedin_jobs_to_db.py'])
print("Instead of running scrapping")
subprocess.run(['DJANGO_SETTINGS_MODULE=career_proj.prod_settings venv/bin/python3','/home/ubuntu/src/career/jobs_scrappers/linkedin_scrapper/get_linkedin_jobs_to_db.py'])