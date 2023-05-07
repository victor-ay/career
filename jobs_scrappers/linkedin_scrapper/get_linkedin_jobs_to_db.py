import json

from LinkedInJobsScraper import LinkedInJobsScraper

from linkedInToDB import LinkedInToDB

with open('../jobs_title_lookup.json', 'r') as fh:
    jobs_title_lookup = json.load(fh)

with open('configs/linkedin_geo_coding.json', 'r') as fh:
    linkedin_geo_coding = json.load(fh)

# with open('configs/linkedin_posting_interval_coding.json', 'r') as fh:
#     linkedin_posting_interval_coding = json.load(fh)

# Sleep time in seconds for random sleep time between requests inside each tasker
min_sec_sleep_between_requests = 12
max_sec_sleep_between_requests = 17

# Scrap jobs that were posted maximum 'day' before
# All options are: ["day" , "week" , "month"]
# The file holding this info: linkedin_posting_interval_coding.json
timePostedRange = 'day'


linkedin_job_taskers = []

# #tester
# job_title_software_developer = ["ios"]
#
# # for test only
# for title,val in jobs_title_lookup.items():
#     for location in linkedin_geo_coding:
#         print(title)
#         print(location)
#         tasker = LinkedInJobsScraper(
#             keywords=job_title_software_developer,
#             location=location,
#             timePostedRange=timePostedRange,
#             min_sec_sleep_between_requests=min_sec_sleep_between_requests,
#             max_sec_sleep_between_requests=max_sec_sleep_between_requests)
#         linkedin_job_taskers.append(tasker)




# Creating taskers to scrap jobs from linkedin according to {location , title, timePostedRange}
for title,val in jobs_title_lookup.items():
    for location in linkedin_geo_coding:
        print(title)
        print(location)
        tasker = LinkedInJobsScraper(
            keywords=jobs_title_lookup[title],
            location=location,
            timePostedRange=timePostedRange,
            min_sec_sleep_between_requests=min_sec_sleep_between_requests,
            max_sec_sleep_between_requests=max_sec_sleep_between_requests)
        linkedin_job_taskers.append(tasker)




file_num = 0
for tasker in linkedin_job_taskers:
    tasker_jobs = tasker.retrieve_jobs_descriptions_from_linkedin()
    # tasker.save_jobs_descriptions_to_file(file_name_start='israel_test_3_'+ str(file_num))
    file_num+=1

    for tasker_job in tasker_jobs:
        db_transporter = LinkedInToDB(dict_25_jobs=tasker_job)
        db_transporter.linkedin_dict_to_db_companies()
        db_transporter.linkedin_dict_to_db_jobs()


def just_hello():
    print("Just hello string")
