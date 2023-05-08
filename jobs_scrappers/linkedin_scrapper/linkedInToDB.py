import datetime
import os
from pprint import pprint

import django

# os.environ['DJANGO_SETTINGS_MODULE'] = 'career_proj.settings'
django.setup()

from djmoney.money import Money
# from rest_framework.authtoken.admin import User
from django.contrib.auth.models import User

import json

from jobs_app.models import Company, Job
from jobs_scrappers.linkedin_scrapper.LinkedInJobsParser import LinkedInJobsParser


class LinkedInToDB():
    def __init__(self, dict_25_jobs: dict):
        self._dict_25_jobs = dict_25_jobs
        self._parsedData = LinkedInJobsParser(dict_25_jobs=self._dict_25_jobs).parse()
        self._dd = 8

    def _get_job_value_or_empty(self,job,attribute,return_default):
        if job.get(attribute):
            return job.get(attribute)
        return return_default


    def linkedin_dict_to_db_companies(self):

        """
        Goes through the dictionary of jobs descriptions "self._dict_25_jobs" (which can consist of max 25 jobs)
        Extracts the relevant information and saves the company instance to the Company table in the DB.
        :return:
        """

        # companyParser = LinkedInJobsParser(dict_25_jobs=self._dict_25_jobs).parse()
        for job_id in self._parsedData:
            job = self._parsedData[job_id]
            # pprint(myParser[job])

            comp_name = job.get('company_name')
            if job.get('company_size_min'):
                comp_employees_min = int(job['company_size_min'])
            else:
                comp_employees_min = None

            if job.get('company_size_max'):
                comp_employees_max = int(job['company_size_max'])
            else:
                comp_employees_max = None

            comp_logo_200_px = self._get_job_value_or_empty(job,'logo_200_px','')
            comp_logo_400_px = self._get_job_value_or_empty(job,'logo_400_px','')
            comp_industry = self._get_job_value_or_empty(job,'company_industry','')
            comp_id_linkedin = self._get_job_value_or_empty(job,'company_id',00000)

            comp_linkedin_url = self._get_job_value_or_empty(job,'company_linkedin_url','')


            nCompany = Company(name=comp_name,
                               industry=comp_industry,
                               company_id_linkedin=comp_id_linkedin,
                               website=None,
                               company_linkedin_url=comp_linkedin_url,
                               employees_min=comp_employees_min,
                               employees_max=comp_employees_max,
                               logo_200_px=comp_logo_200_px,
                               logo_400_px=comp_logo_400_px,
                               user_id =2
                               )
            if not Company.objects.filter(company_id_linkedin=comp_id_linkedin):
                try:
                    nCompany.save()
                except Exception as e:
                    print(f"Could not save the Company. Excepted: {e}")



    def linkedin_dict_to_db_jobs(self):

        # jobParser = LinkedInJobsParser(dict_25_jobs=self._dict_25_jobs).parse()
        for job_id in self._parsedData:
            job = self._parsedData[job_id]

            j_source = 'LinkedIn'
            j_source_id = job['job_id']
            j_is_active = True

            # if 'remote' in job['job_location'].lower() or 'virtual' in job['job_location'].lower():
            #     j_employment_type = 'Remote'
            # elif 'hybrid' in job['job_location'].lower():
            #     j_employment_type = 'Hybrid'
            # else:
            #     j_employment_type = 'On-site'

            j_employment_type = self._get_job_value_or_empty(job, 'job_employment_type', 'Employee')
            j_employment_percent = self._get_job_value_or_empty(job, 'employment_percent', 'Full-time')
            j_level = self._get_job_value_or_empty(job, 'job_level', None)

            if j_level == 'Internship':
                j_type = 'Internship'
            else:
                j_type = 'Employee'

            j_application_url =self._get_job_value_or_empty(job, 'apply_url', '')
            j_description = self._get_job_value_or_empty(job, 'job_description', '')
            j_location = self._get_job_value_or_empty(job, 'job_location', '')
            j_title = self._get_job_value_or_empty(job, 'job_title', '')
            j_max_payment = self._get_job_value_or_empty(job, 'max_payment', None)
            j_min_payment = self._get_job_value_or_empty(job, 'min_payment', None)
            j_level = self._get_job_value_or_empty(job, 'job_level', None)

            j_posted_epoch = self._get_job_value_or_empty(job, 'posted_epoch', int(datetime.datetime.now().strftime('%s'))*1000)


            job_payment_period =  self._get_job_value_or_empty(job, 'payment_period', None)
            if job_payment_period == 'yr':
                j_payment_period = 'Annually'
            elif job_payment_period == 'mn':
                j_payment_period = 'Monthly'
            elif job_payment_period == 'hr':
                j_payment_period = 'Hourly'
            else:
                j_payment_period = None

            comp_id_linkedin =  self._get_job_value_or_empty(job, 'company_id', None)

            qs_company =  Company.objects.filter(company_id_linkedin=comp_id_linkedin)
            if len(qs_company)>0:
                the_company = qs_company[0]

                the_recruiter = User.objects.get(id=1)

                n_job = Job(
                    company=the_company,
                    recruiter=the_recruiter,
                    source=j_source,
                    source_job_id=j_source_id,
                    is_active=j_is_active,
                    employment_type=j_employment_type,
                    employment_percent=j_employment_percent,
                    job_type=j_type,
                    job_level=j_level,
                    payment_period=j_payment_period,
                    title=j_title,
                    description=j_description,
                    location=j_location,
                    posted_on_epoch=j_posted_epoch / 1000,
                    application_url=j_application_url,
                    posted_on=datetime.datetime.fromtimestamp(j_posted_epoch / 1000),
                    closed_at=None

                )
                if j_min_payment:
                    n_job.payment_min = Money(str(j_min_payment), "USD")

                if j_max_payment:
                    n_job.payment_max = Money(str(j_max_payment), "USD")


                try:
                    n_job.save()
                except Exception as e:
                    print(f"Could not save the Job to the DB. Exception: {e}")


if __name__ == '__main__':
    # l = ''
    with open('scraped_files/israel_test_4_noTitle-2023-05-03.json', 'r') as fh:
        all_file = json.load(fh)

    print(len(all_file))

    for jset in all_file:
        # print(jset)
        db_transporter = LinkedInToDB(dict_25_jobs=jset)
        db_transporter.linkedin_dict_to_db_companies()
        db_transporter.linkedin_dict_to_db_jobs()
