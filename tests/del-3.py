import json
import re
from pprint import pprint

with open ('../linkedin_scrapper/scraped_files/israel_test_2-13-03-2023.json', 'r') as fh:
    all_file = json.load(fh)

# pprint(all_file[1])
found_navigationBarSubtitle =0
found_hasConfirmedEmailAddress =0
found_jobDetailsSummaryCard =0

for i in range(len(all_file[1]['included'])):
    for keys, values in all_file[1]["included"][i].items():
        if  "navigationBarSubtitle" in keys:
            found_navigationBarSubtitle+=1
            print(f'navigationBarSubtitle'
                  f'i = {i}\n'
                  f'{all_file[1]["included"][i]["entityUrn"]}\n')

        if keys == "hasConfirmedEmailAddress":
            found_hasConfirmedEmailAddress += 1
            print(f'hasConfirmedEmailAddress'
                  f'i = {i}\n'
                  f'{all_file[1]["included"][i]["entityUrn"]}\n')

        if keys == "*jobDetailsSummaryCard":
            found_jobDetailsSummaryCard += 1
            print(f'*jobDetailsSummaryCard'
                  f'i = {i}\n'
                  f'{all_file[1]["included"][i]["entityUrn"]}\n')

print(f"found_navigationBarSubtitle = {found_navigationBarSubtitle}\n"
      f"found_hasConfirmedEmailAddress = {found_hasConfirmedEmailAddress}\n"
      f"found_jobDetailsSummaryCard = {found_jobDetailsSummaryCard}")
# pprint((all_file[1]["included"][0].keys()))
# k1 = all_file[1]
#
# job_obj = {}
#
# job_num = 3519985358
# company_id = 35710155
#
# tt=''
#
# for i in range (len(all_file[1]["included"])-1):
#     k2 = []
#     for keys, values in k1["included"][i].items():
#         k2.append(keys)
#         if k1["included"][i]["$type"] == "com.linkedin.voyager.dash.organization.Company" and str(company_id) in k1["included"][i]['entityUrn'] :
#             print("\n","&"*150)
#             pprint(k1["included"][i])


    # print(k2)

# print("*"*150)
# # print(f"i = {mi}")
# pprint(job_obj,indent=6)


# def format_LinkedIn_job_description(format_list, description:str) -> str:
#     descr_list = list(description)
#     paragraph_collector =0
#
#     for i in range(len(format_list)-1):
#         format_style = format_list[i]['detailDataUnion']['style']
#         format_start = format_list[i]['start']
#         format_length = format_list[i]['length']
#
#         if format_style == 'PARAGRAPH':
#             paragraph_collector = paragraph_collector + format_length
#             descr_list.insert(paragraph_collector + format_start,"\n")
#
#         if format_style == 'LIST_ITEM':
#
#             descr_list.insert(paragraph_collector + format_start,"\n\t")
#             paragraph_collector = paragraph_collector + 1
#
#     return ''.join(descr_list)

# print(format_LinkedIn_job_description( format_list=text_format , description=text_init))
# print(text_init)