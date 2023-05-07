import json

print("Hello from (print_hello)")
with open('linkedin_scrapper/scraped_files/israel_test_4_noTitle-2023-05-03.json', 'r') as fh:
    all_file = json.load(fh)

print(f"File length  = {len(all_file)}")