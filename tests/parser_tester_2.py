import json
from pprint import pprint

from jobs_scrappers.linkedin_scrapper.LinkedInJobsParser import LinkedInJobsParser

with open('../jobs_scrappers/linkedin_scrapper/scraped_files/israel_test_4_1-2023-05-03.json', 'r') as fh:
    all_file = json.load(fh)

myParser = LinkedInJobsParser(dict_25_jobs=all_file[0]).parse()
pprint(myParser)