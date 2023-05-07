import json

from jobs_scrappers.linkedin_scrapper.LinkedInToDB import LinkedInToDB

print("Hello from (print_hello)")
with open('linkedin_scrapper/scraped_files/israel_test_4_noTitle-2023-05-03.json', 'r') as fh:
    all_file = json.load(fh)

print(f"File length  = {len(all_file)}")

for jset in all_file:
    print(f"Inside loop over all_file")
    db_transporter = LinkedInToDB(dict_25_jobs=jset)
    print(f"After db_transporter = LinkedInToDB(dict_25_jobs=jset)")
    # db_transporter.linkedin_dict_to_db_companies()
    # db_transporter.linkedin_dict_to_db_jobs()