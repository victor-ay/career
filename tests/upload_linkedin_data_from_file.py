import datetime
import os

import os


import django


os.environ['DJANGO_SETTINGS_MODULE'] = 'career_proj.settings'
django.setup()

from djmoney.money import Money
# from rest_framework.authtoken.admin import User
from django.contrib.auth.models import User

from decimal import Decimal
import json
from pprint import pprint

from jobs_app.models import Company, Job
from linkedin_scrapper.LinkedInJobsParser import LinkedInJobsParser

with open('../linkedin_scrapper/scraped_files/israel_test_2-13-03-2023.json', 'r') as fh:
    all_file = json.load(fh)

def none_or_typed_context(obj, cont_type):
    if obj:
        return cont_type(obj)
    return None

def LinkedInDictToDB_companies(jobsDict: dict):

    myParser = LinkedInJobsParser(dict_25_jobs=jobsDict).parse()
    for job_id in myParser:
        job = myParser[job_id]
        # pprint(myParser[job])

        comp_name = job['company_name']
        if job['company_size_min']:
            comp_employees_min = int(job['company_size_min'])
        else:
            comp_employees_min = None

        if job['company_size_max']:
            comp_employees_max = int(job['company_size_max'])
        else:
            comp_employees_max = None

        comp_logo_200_px = job['logo_200_px']
        comp_logo_400_px = job['logo_400_px']
        comp_industry = job['company_industry']
        comp_id_linkedin = job['company_id']
        comp_linkedin_url = job['company_linkedin_url']

        nCompany = Company(name = comp_name,
                           industry = comp_industry,
                           company_id_linkedin = comp_id_linkedin,
                           website = None,
                           company_linkedin_url = comp_linkedin_url,
                           employees_min = comp_employees_min,
                           employees_max = comp_employees_max,
                           logo_200_px = comp_logo_200_px,
                           logo_400_px = comp_logo_400_px
                           )
        nCompany.save()


def LinkedInDictToDB_jobs(jobsDict: dict):

    myParser = LinkedInJobsParser(dict_25_jobs=jobsDict).parse()
    for job_id in myParser:
        job = myParser[job_id]

        j_source = 'LinkedIn'
        j_source_id = job['job_id']
        j_is_active = True

        if 'remote' in job['job_location'].lower() or 'virtual' in job['job_location'].lower():
            j_employment_type = 'Remote'
        elif 'hybrid' in job['job_location'].lower():
            j_employment_type = 'Hybrid'
        else:
            j_employment_type = 'On-site'

        j_employment_percent = job['employment_percent']
        j_level = job['job_level']

        if j_level == 'Internship':
            j_type = 'Internship'
        else:
            j_type = 'Employee'


        j_application_url = job['apply_url']
        j_description = job['job_description']
        j_location = job['job_location']
        j_title = job['job_title']
        j_max_payment = job['max_payment']
        j_min_payment = job['min_payment']

        # if job['max_payment']:
        #     j_max_payment_amount = Decimal(job['max_payment'])
        # else:
        #     j_max_payment_amount = Decimal("2.22")
        # j_max_payment_currency = "USD"
        #
        # if job['min_payment']:
        #     j_min_payment_amount = Decimal(job['min_payment'])
        # else:
        #     j_min_payment_amount = Decimal("3.33")

        # j_min_payment_currency = "USD"

        # j_min_payment = Money(job['min_payment'],"USD")

        j_posted_epoch = job['posted_epoch']
        # if job['min_max_payment_currency'] == '$':
        #     j_currency = 'USD'
        # else:
        #     j_currency='USD'

        if job['payment_period'] == 'yr':
            j_payment_period = 'Annually'
        elif job['payment_period'] == 'mn':
            j_payment_period = 'Monthly'
        elif job['payment_period'] == 'hr':
            j_payment_period = 'Hourly'
        else:
            j_payment_period = None

        comp_id_linkedin = job['company_id']
        the_company = Company.objects.filter(company_id_linkedin = comp_id_linkedin)[0]
        the_recruiter = User.objects.get(id=2)


        n_job = Job(
            company = the_company,
            recruiter = the_recruiter,
            source = j_source,
            source_job_id = j_source_id,
            is_active = j_is_active,
            employment_type = j_employment_type,
            employment_percent = j_employment_percent,
            job_type = j_type,
            payment_period = j_payment_period,
            title = j_title,
            description = j_description,
            location=j_location,
            posted_on_epoch=j_posted_epoch/1000,
            application_url=j_application_url,
            posted_on = datetime.datetime.fromtimestamp(j_posted_epoch/1000),
            closed_at = None
        )
        if j_min_payment:
            n_job.payment_min = Money(str(j_min_payment), "USD")

        if j_max_payment:
            n_job.payment_max = Money(str(j_max_payment), "USD")

        n_job.save()

        # break

        # print(f"epoch = {job['posted_epoch']/1000}")
        # try:
        #     print(f"posted on : {datetime.datetime.fromtimestamp(j_posted_epoch/1000)}")
        # except:
        #     pass


if __name__ == '__main__':

    # transfer_companies = LinkedInDictToDB_companies(jobsDict = all_file[1])
    transfer_jobs = LinkedInDictToDB_jobs(jobsDict=all_file[1])