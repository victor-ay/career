import json
import re
from pprint import pprint


class LinkedInJobsParser():
    """
    Recieves dictionary with up to 25 jobs descriptions.
    Returns list of dictionaries with parsed jobs description
    """
    def __init__(self, dict_25_jobs : dict):
        self._initial_25_jobs_dict = dict_25_jobs
        self._jobs_id_dict = {}
        self._numb_of_ids = len(self._initial_25_jobs_dict['data']['elements'])
        
        self._jobs_obj = {}

    @staticmethod
    def _get_first_number_from_string(text:str)->str:
        matcher = re.findall('\d+',text)
        if len(matcher)>0:
            return matcher[0]
        return '0'

    @staticmethod
    def _format_LinkedIn_job_description(format_list, description: str) -> str:
        descr_list = list(description)
        paragraph_collector = 0

        for i in range(len(format_list) - 1):
            format_style = format_list[i]['detailDataUnion']['style']
            format_start = format_list[i]['start']
            format_length = format_list[i]['length']
            # format_end = format_list[i]['start']+format_list[i]['length']

            if format_style == 'PARAGRAPH':
                paragraph_collector = paragraph_collector + format_length
                descr_list.insert(paragraph_collector + format_start, "\n")

            if format_style == 'LIST_ITEM':
                descr_list.insert(paragraph_collector + format_start, "\n\t")
                paragraph_collector = paragraph_collector + 1

        return ''.join(descr_list)

    def _initiate_dict_of_jobs(self)-> dict:
        for i in range(self._numb_of_ids):
            job_id_str = self._initial_25_jobs_dict['data']['elements'][i]['jobCardUnion']['*jobPostingCard']
            self._jobs_id_dict[self._get_first_number_from_string(job_id_str)]={}

        return self._jobs_id_dict

    def _put_description_field_or_none(self, job_id:str, key: str, value , default = None):
        if value:
            self._jobs_id_dict[job_id][key]=value
        else:
            self._jobs_id_dict[job_id][key] = default

    def parse(self):
        self._initiate_dict_of_jobs()
        for i in range(len(self._initial_25_jobs_dict['included'])):
            for keys, values in self._initial_25_jobs_dict["included"][i].items():

                short_include = self._initial_25_jobs_dict["included"][i]
                entityUrn_str = self._initial_25_jobs_dict["included"][i]['entityUrn']

                job_num = self._get_first_number_from_string(entityUrn_str)

                if len(job_num)>3:

                    if "navigationBarSubtitle" in keys:
                        self._put_description_field_or_none(
                            job_id=job_num,
                            key="job_id",
                            value=re.findall('[0-9]+', short_include["*jobPosting"])[0]
                        )
                        self._put_description_field_or_none(
                            job_id=job_num,
                            key="company_linkedin_url",
                            value=short_include['companyLogo']['actionTarget']
                        )

                        # find in company object
                        self._put_description_field_or_none(
                            job_id=job_num,
                            key="company_id",
                            value=re.findall('[0-9]+', short_include['companyLogo']['attributes'][0]['detailData']['*companyLogo'])[0]
                        )
                        self._put_description_field_or_none(
                            job_id=job_num,
                            key="posted_epoch",
                            value=short_include['primaryDescription']['attributesV2'][3]['detailDataUnion']['epoch']['epochAt']
                        )
                        self._put_description_field_or_none(
                            job_id=job_num,
                            key="job_location",
                            value=short_include["navigationBarSubtitle"].split("·")[1].strip()
                        )

                        self._put_description_field_or_none(
                            job_id=job_num,
                            key="company_name",
                            value=short_include["navigationBarSubtitle"].split("·")[0].strip()
                        )


                        type_of_job_list = short_include["jobInsightsV2"][0]['insightViewModel']['text']['text'].split("·")
                        if len(type_of_job_list)>0:
                            self._put_description_field_or_none(
                                job_id=job_num,
                                key="job_type",
                                value=type_of_job_list[0].strip()
                            )
                        if len(type_of_job_list)>1:
                            self._put_description_field_or_none(
                                job_id=job_num,
                                key="job_level",
                                value=type_of_job_list[1].strip()
                            )



                        type_of_company_list = short_include["jobInsightsV2"][1]['insightViewModel']['text']['text'].split("·")
                        if len(type_of_company_list)>0:
                            self._put_description_field_or_none(
                                job_id=job_num,
                                key="company_size_min_max",
                                value=re.findall('\d+',re.sub(',', '', type_of_company_list[0].strip()))
                            )

                        if len(type_of_company_list) > 1:
                            self._put_description_field_or_none(
                                job_id=job_num,
                                key="company_industry",
                                value=type_of_company_list[1].strip()
                            )

                        # self._jobs_obj["job_title"] = short_include["jobPostingTitle"]

                        self._put_description_field_or_none(
                            job_id = job_num,
                            key = "job_title",
                            value = short_include["jobPostingTitle"]
                        )

                    if keys == "hasConfirmedEmailAddress":
                        # self._jobs_obj["apply_url"] = short_include['companyApplyUrl']
                        self._put_description_field_or_none(
                            job_id = job_num,
                            key = "apply_url",
                            value = short_include['companyApplyUrl']
                        )

                    if keys == "*jobDetailsSummaryCard":
                        text_init = short_include['description']['text']
                        text_format = short_include['description']['attributesV2']
                        # self._jobs_obj["job_description"] = self._format_LinkedIn_job_description(format_list=text_format,
                        #                                                              description=text_init)
                        self._put_description_field_or_none(
                            job_id = job_num,
                            key = "job_description",
                            value = self._format_LinkedIn_job_description(format_list=text_format,
                                                                                     description=text_init)
                        )

                try:
                    logo_root_url = short_include['logo']['vectorImage']['rootUrl']

                    company_id = self._get_first_number_from_string(self._initial_25_jobs_dict["included"][i]['entityUrn'])
                    for key, value in self._jobs_id_dict.items():
                        if str(value['company_id']) == str(company_id):
                            job_num = key
                            break

                    self._put_description_field_or_none(
                        job_id=job_num,
                        key="logo_100_px",
                        value=logo_root_url + short_include['logo']['vectorImage']['artifacts'][1][
                        'fileIdentifyingUrlPathSegment']
                    )
                    self._put_description_field_or_none(
                        job_id=job_num,
                        key="logo_200_px",
                        value= logo_root_url + short_include['logo']['vectorImage']['artifacts'][0][
                        'fileIdentifyingUrlPathSegment']
                    )
                    self._put_description_field_or_none(
                        job_id=job_num,
                        key="logo_400_px",
                        value= logo_root_url + short_include['logo']['vectorImage']['artifacts'][2][
                        'fileIdentifyingUrlPathSegment']
                    )
                except Exception as e:
                    pass
                    # print(e)

                    # print(f"&&&")

        return self._jobs_id_dict
        # pprint(self._jobs_id_dict)

    def __str__(self):
        return f"{self._jobs_obj}"

if __name__ == '__main__':
    with open('scraped_files/israel_test_2-13-03-2023.json', 'r') as fh:
        all_file = json.load(fh)
        
    myParser = LinkedInJobsParser(dict_25_jobs=all_file[1]).parse()
    pprint(myParser)

