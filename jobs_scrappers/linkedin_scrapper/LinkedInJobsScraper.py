import datetime
import json
import os
import random
import re
import time
from pprint import pprint

import urllib.request

import requests

import django


# os.environ['DJANGO_SETTINGS_MODULE'] = 'career_proj.settings'
django.setup()

from jobs_app.models import Job
from jobs_scrappers.linkedin_scrapper.LinkedInHeaderCoockieHandler import LinkedInHeaderHandler
from jobs_scrappers.linkedin_scrapper.LinkedInHeaderQueue import LinkedInHeaderQueue

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    'csrf-token': 'ajax:2918111014867513287',
    'cookie':
        'bcookie="v=2&f73a89e2-296c-470c-8724-91d19e695678"; bscookie="v=1&2022062121132628309a49-e964-42c8-88ec-f6a6d94722e9AQFJqCAIKyye1dN5lYrnhLLbUV4Y-HhQ"; JSESSIONID="ajax:2918111014867513287"; li_theme=light; li_theme_set=app; li_sugr=86e86bdd-e3bf-4e97-bbb4-23024dccfe3b; _gcl_au=1.1.361179661.1655846165; g_state={"i_l":0}; G_ENABLED_IDPS=google; lang=v=2&lang=en-us; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; G_AUTHUSER_H=0; _guid=fee4813e-03bf-4a65-8d27-42d0364e3c81; aam_uuid=30722516814145316542175151343104450939; timezone=Asia/Jerusalem; AnalyticsSyncHistory=AQKpnerv7EOAeQAAAYaJYEF39tjSd40JQ6tX2RNuBtHEjdbULA3UY00tAuzrdv2M0MOXIPyBTorJyzoGELynsg; lms_ads=AQER4OYz83zjFAAAAYaJYEJsb7SmmSxT5xtfZ3rSZm2oMKQvht_mXctmcrNDd2HKu3sKUdaos4NnPmiFMGCUZeUE77VAUCoI; lms_analytics=AQER4OYz83zjFAAAAYaJYEJsb7SmmSxT5xtfZ3rSZm2oMKQvht_mXctmcrNDd2HKu3sKUdaos4NnPmiFMGCUZeUE77VAUCoI; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19414%7CMCMID%7C30573763729732222852224953742619742896%7CMCAAMLH-1677946833%7C6%7CMCAAMB-1677946833%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1677349233s%7CNONE%7CvVersion%7C5.1.1%7CMCCIDH%7C1845937615; liap=true; li_at=AQEDATRluvgF23xpAAABhol0VksAAAGGrYDaS00Ag3hHJnHOFGDMFXiISVI_WDx2GM-QORJH-gPE4Dv-gon-5pCvVkCoC_zYwelrCOaCi7L1BG5MBziI6-N7fFxtNyyoIL-QteGESCmdLnLIiy-jzs8u; sdsc=22%3A1%2C1677343354488%7EJAPP%2C0ugR%2FXz5Ovh%2BBmZLcwEEtpOl5dfU%3D; UserMatchHistory=AQJbpyIYx7w1lgAAAYaJd8TJPe3KYlAWaQOhu8zt4RdC3mMlv770oseZb8xQ2sxGiwmZMVyoqPLZ6RsXHK6O1LKqg8QuMyGqBauBrzED26-sCB5fIcMlxkqpzF3nLbThniParCsvOOaUdcAabETnpp0UkBn1ggzxIvk7uqNAHOTgOwM5MFareEtxB-vsw-PVr1lP0irERilVHuKWeRUidCnpJ9NPHmlxlOWTQp6_fUhs3CCR2WUW0chC3Q_EL1TnahJDHJNkof51ZLlspnFQEFPSbZotN920nWasA64; lidc="b=VB32:s=V:r=V:a=V:p=V:g=4235:u=88:x=1:i=1677343573:t=1677427555:v=2:sig=AQFK6oI9sUnPhwPVX6ujOq5u4z4lLGF-"'
        ,
    'authority': 'www.linkedin.com',
    'accept': 'application/vnd.linkedin.normalized+json+2.1',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'referer': 'https://www.linkedin.com/jobs/search/?currentJobId=3090136770&geoId=101620260',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "Windows",
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'x-kl-ajax-request': 'Ajax_Request',
    'x-li-deco-include-micro-schema': 'true',
    'x-li-lang': 'en_US',
    'x-li-page-instance': 'urn:li:page:d_flagship3_search_srp_jobs;+p7hKFbPQXysO4sepSgopQ==',
    'x-li-track': '{"clientVersion":"1.10.6174","mpVersion":"1.10.6174","osName":"web","timezoneOffset":3,"timezone":"Asia/Jerusalem","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1,"displayWidth":1920,"displayHeight":1080}',
    'x-restli-protocol-version': '2.0.0'
    }

#     'cookie':
#         'bcookie="v=2&f73a89e2-296c-470c-8724-91d19e695678"; bscookie="v=1&2022062121132628309a49-e964-42c8-88ec-f6a6d94722e9AQFJqCAIKyye1dN5lYrnhLLbUV4Y-HhQ"; JSESSIONID="ajax:2918111014867513287"; li_theme=light; li_theme_set=app; li_sugr=86e86bdd-e3bf-4e97-bbb4-23024dccfe3b; _gcl_au=1.1.361179661.1655846165; g_state={"i_l":0}; G_ENABLED_IDPS=google; lang=v=2&lang=en-us; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; G_AUTHUSER_H=0; _guid=fee4813e-03bf-4a65-8d27-42d0364e3c81; aam_uuid=30722516814145316542175151343104450939; timezone=Asia/Jerusalem; AnalyticsSyncHistory=AQKpnerv7EOAeQAAAYaJYEF39tjSd40JQ6tX2RNuBtHEjdbULA3UY00tAuzrdv2M0MOXIPyBTorJyzoGELynsg; lms_ads=AQER4OYz83zjFAAAAYaJYEJsb7SmmSxT5xtfZ3rSZm2oMKQvht_mXctmcrNDd2HKu3sKUdaos4NnPmiFMGCUZeUE77VAUCoI; lms_analytics=AQER4OYz83zjFAAAAYaJYEJsb7SmmSxT5xtfZ3rSZm2oMKQvht_mXctmcrNDd2HKu3sKUdaos4NnPmiFMGCUZeUE77VAUCoI; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19414%7CMCMID%7C30573763729732222852224953742619742896%7CMCAAMLH-1677946833%7C6%7CMCAAMB-1677946833%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1677349233s%7CNONE%7CvVersion%7C5.1.1%7CMCCIDH%7C1845937615; liap=true; li_at=AQEDATRluvgF23xpAAABhol0VksAAAGGrYDaS00Ag3hHJnHOFGDMFXiISVI_WDx2GM-QORJH-gPE4Dv-gon-5pCvVkCoC_zYwelrCOaCi7L1BG5MBziI6-N7fFxtNyyoIL-QteGESCmdLnLIiy-jzs8u; sdsc=22%3A1%2C1677343354488%7EJAPP%2C0ugR%2FXz5Ovh%2BBmZLcwEEtpOl5dfU%3D; UserMatchHistory=AQJbpyIYx7w1lgAAAYaJd8TJPe3KYlAWaQOhu8zt4RdC3mMlv770oseZb8xQ2sxGiwmZMVyoqPLZ6RsXHK6O1LKqg8QuMyGqBauBrzED26-sCB5fIcMlxkqpzF3nLbThniParCsvOOaUdcAabETnpp0UkBn1ggzxIvk7uqNAHOTgOwM5MFareEtxB-vsw-PVr1lP0irERilVHuKWeRUidCnpJ9NPHmlxlOWTQp6_fUhs3CCR2WUW0chC3Q_EL1TnahJDHJNkof51ZLlspnFQEFPSbZotN920nWasA64; lidc="b=VB32:s=V:r=V:a=V:p=V:g=4235:u=88:x=1:i=1677429322:t=1677514077:v=2:sig=AQHvtXPtAuLxyLFs70c9TbPReYMs19yO"'
#         ,

# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
#     'csrf-token': 'ajax:2918111014867513287',
#
#     'authority': 'www.linkedin.com',
#     'accept': 'application/vnd.linkedin.normalized+json+2.1',
#     'accept-encoding': 'gzip, deflate, br',
#     'accept-language': 'en-US,en;q=0.9',
#     'referer': 'https://www.linkedin.com/jobs/search/?currentJobId=3090136770&geoId=101620260',
#     'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
#     'sec-ch-ua-mobile': '?0',
#     'sec-ch-ua-platform': "Windows",
#     'sec-fetch-dest': 'empty',
#     'sec-fetch-mode': 'cors',
#     'sec-fetch-site': 'same-origin',
#     'x-kl-ajax-request': 'Ajax_Request',
#     'x-li-deco-include-micro-schema': 'true',
#     'x-li-lang': 'en_US',
#     'x-li-page-instance': 'urn:li:page:d_flagship3_search_srp_jobs;+p7hKFbPQXysO4sepSgopQ==',
#     'x-li-track': '{"clientVersion":"1.10.6174","mpVersion":"1.10.6174","osName":"web","timezoneOffset":3,"timezone":"Asia/Jerusalem","deviceFormFactor":"DESKTOP","mpName":"voyager-web","displayDensity":1,"displayWidth":1920,"displayHeight":1080}',
#     'x-restli-protocol-version': '2.0.0'
#     }

# look for :
# voyagerJobsDashJobCards

cookie_out ='bcookie="v=2&f73a89e2-296c-470c-8724-91d19e695678"; bscookie="v=1&2022062121132628309a49-e964-42c8-88ec-f6a6d94722e9AQFJqCAIKyye1dN5lYrnhLLbUV4Y-HhQ"; JSESSIONID="ajax:2918111014867513287"; li_theme=light; li_theme_set=app; li_sugr=86e86bdd-e3bf-4e97-bbb4-23024dccfe3b; _gcl_au=1.1.361179661.1655846165; g_state={"i_l":0}; G_ENABLED_IDPS=google; lang=v=2&lang=en-us; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; G_AUTHUSER_H=0; _guid=fee4813e-03bf-4a65-8d27-42d0364e3c81; aam_uuid=30722516814145316542175151343104450939; timezone=Asia/Jerusalem; AnalyticsSyncHistory=AQKpnerv7EOAeQAAAYaJYEF39tjSd40JQ6tX2RNuBtHEjdbULA3UY00tAuzrdv2M0MOXIPyBTorJyzoGELynsg; lms_ads=AQER4OYz83zjFAAAAYaJYEJsb7SmmSxT5xtfZ3rSZm2oMKQvht_mXctmcrNDd2HKu3sKUdaos4NnPmiFMGCUZeUE77VAUCoI; lms_analytics=AQER4OYz83zjFAAAAYaJYEJsb7SmmSxT5xtfZ3rSZm2oMKQvht_mXctmcrNDd2HKu3sKUdaos4NnPmiFMGCUZeUE77VAUCoI; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19414%7CMCMID%7C30573763729732222852224953742619742896%7CMCAAMLH-1677946833%7C6%7CMCAAMB-1677946833%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1677349233s%7CNONE%7CvVersion%7C5.1.1%7CMCCIDH%7C1845937615; liap=true; li_at=AQEDATRluvgF23xpAAABhol0VksAAAGGrYDaS00Ag3hHJnHOFGDMFXiISVI_WDx2GM-QORJH-gPE4Dv-gon-5pCvVkCoC_zYwelrCOaCi7L1BG5MBziI6-N7fFxtNyyoIL-QteGESCmdLnLIiy-jzs8u; sdsc=22%3A1%2C1677343354488%7EJAPP%2C0ugR%2FXz5Ovh%2BBmZLcwEEtpOl5dfU%3D; UserMatchHistory=AQJbpyIYx7w1lgAAAYaJd8TJPe3KYlAWaQOhu8zt4RdC3mMlv770oseZb8xQ2sxGiwmZMVyoqPLZ6RsXHK6O1LKqg8QuMyGqBauBrzED26-sCB5fIcMlxkqpzF3nLbThniParCsvOOaUdcAabETnpp0UkBn1ggzxIvk7uqNAHOTgOwM5MFareEtxB-vsw-PVr1lP0irERilVHuKWeRUidCnpJ9NPHmlxlOWTQp6_fUhs3CCR2WUW0chC3Q_EL1TnahJDHJNkof51ZLlspnFQEFPSbZotN920nWasA64; lidc="b=VB32:s=V:r=V:a=V:p=V:g=4235:u=88:x=1:i=1677429322:t=1677514077:v=2:sig=AQHvtXPtAuLxyLFs70c9TbPReYMs19yO"'



# with open('linkedIn_cookies.json', 'r') as ch:
#     cookies = json.load(ch)
# pprint(type(cookies))

pgUrl_base = "https://www.linkedin.com/voyager/api/search/hits?decorationId=com.linkedin.voyager.deco.jserp.WebJobSearchHitWithSalary-25&count=25&filters=List(locationFallback-%3EIsrael,geoUrn-%3Eurn%3Ali%3Afs_geo%3A101620260,resultType-%3EJOBS)&keywords=Junior%20Developer&origin=JOB_SEARCH_PAGE_OTHER_ENTRY&q=jserpFilters&queryContext=List(primaryHitType-%3EJOBS,spellCorrectionEnabled-%3Etrue)&start=100&topNRequestedFlavors=List(HIDDEN_GEM,IN_NETWORK,SCHOOL_RECRUIT,COMPANY_RECRUIT,SALARY,JOB_SEEKER_QUALIFIED,PRE_SCREENING_QUESTIONS,SKILL_ASSESSMENTS,ACTIVELY_HIRING_COMPANY,TOP_APPLICANT)"


# detailed urls
url = "https://www.linkedin.com/voyager/api/graphql?includeWebMetadata=true&variables=" \
      "(jobCardPrefetchQuery:" \
      "(jobUseCase:JOB_DETAILS,prefetchJobPostingCardUrns:" \
      "List(" \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283487756623%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283490896727%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283493055284%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283493734615%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283490999856%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283489177978%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283488601799%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283492113695%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283484863460%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283490998761%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283487754851%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283490362989%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283490318310%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283487239665%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283494162718%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283473306568%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283484275151%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283493769790%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283490315514%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283489443475%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283489119265%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283493057033%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283493056256%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283499554216%2CJOB_DETAILS%29," \
      "urn%3Ali%3Afsd_jobPostingCard%3A%283493773229%2CJOB_DETAILS%29)))&&queryId=voyagerJobsDashJobCards.93b5842d6b28e0031a69345d046ea8d9"

# Posted past week
# https://www.linkedin.com/voyager/api/search/
# hits?decorationId=com.linkedin.voyager.deco.jserp.WebJobSearchHitWithSalary-25&count=25&filters=
# List(timePostedRange-%3Er604800,geoUrn-%3Eurn%3Ali%3Afs_geo%3A101620260,
# sortBy-%3ER,resultType-%3EJOBS)
# &keywords=software%20engineer&origin=JOB_SEARCH_PAGE_JOB_FILTER
# &q=jserpFilters&queryContext=List(primaryHitType-%3EJOBS,spellCorrectionEnabled-%3Etrue)&
# start=25&topNRequestedFlavors=List
# (HIDDEN_GEM,IN_NETWORK,SCHOOL_RECRUIT,COMPANY_RECRUIT,SALARY,JOB_SEEKER_QUALIFIED,PRE_SCREENING_QUESTIONS,SKILL_ASSESSMENTS,ACTIVELY_HIRING_COMPANY,TOP_APPLICANT)


class LinkedInJobsScraper():

    def __init__(self, keywords: [str],
                 location:str,
                 min_sec_sleep_between_requests: int,
                 max_sec_sleep_between_requests: int,
                 # linkedin_header_file : str,
                 timePostedRange = 'week', # => When job was posted. "week" -> in the last week. options are: day, week, month
                 worker_map_file = "configs/linkedin_headers_map.json"
                 ):

        # each keyword => {'keyword' : {
        #                               'start' : int ,
        #                               'tot_jobs_num' : int , // Number of jobs ids per "initial_link" or per "keyword"
        #                               'initial_link' : str  // Url to start exporting ids of jobs
        #                               }
        #                  }

        self._headerQ = LinkedInHeaderQueue(header_map_file=worker_map_file)

        self._linkedin_header_file = self._headerQ.get_next_header_file()
        self._headerHandler = LinkedInHeaderHandler(
            header_file_name=self._linkedin_header_file)
        self._headers = self._headerHandler.get_headers()


        self._keywords = keywords
        self._keywords_ids_info = {} # Dictionary according to keywords.
        for keyword in keywords:
            self._keywords_ids_info[keyword] = {}
            self._keywords_ids_info[keyword]['start'] = None
            self._keywords_ids_info[keyword]['tot_jobs_num'] = None
            self._keywords_ids_info[keyword]['initial_link'] = None

        self._max_sec_sleep_between_requests = max_sec_sleep_between_requests
        self._min_sec_sleep_between_requests = min_sec_sleep_between_requests

        self._tot_jobs_num = None

        try:
            with open('configs/linkedin_posting_interval_coding.json', 'r') as fh:
                timePostedRange_coding = json.load(fh)
                self._timePostedRange = timePostedRange_coding[timePostedRange]
        except Exception as e:
            print(e)




        self._location = location.strip().capitalize()
        self._extracted_jobs_id = 0
        self._jobs_id_list = []
        self._jobs_id_link_list = [] # Each link will have inside max 25 ids
        self._links_25_jobs_description = []
        self._list_of_jobs_description = []

        with open("configs/linkedin_geo_coding.json") as fh:
            self._geo_coding = json.load(fh)

        self._base_url_to_get_jobs_ids = 'https://www.linkedin.com/voyager/api/search/' \
                          'hits?decorationId=com.linkedin.voyager.deco.jserp.WebJobSearchHitWithSalary-25' \
                          '&count=25' \
                          '&origin=JOB_SEARCH_PAGE_JOB_FILTER' \
                          '&q=jserpFilters&queryContext=List(' \
                                        'primaryHitType-%3EJOBS,' \
                                        'spellCorrectionEnabled-%3Etrue)' \
                          '&topNRequestedFlavors=List(' \
                                        'HIDDEN_GEM,IN_NETWORK,SCHOOL_RECRUIT,COMPANY_RECRUIT,SALARY,JOB_SEEKER_QUALIFIED,PRE_SCREENING_QUESTIONS,SKILL_ASSESSMENTS,ACTIVELY_HIRING_COMPANY,TOP_APPLICANT)' \
                         # '&keywords=software%20engineer' \
                         # '&filters=List(' \
                         # '             timePostedRange-%3Er604800,' \
                         #'              locationFallback - % 3EIsrael,'\
                         # '             geoUrn-%3Eurn%3Ali%3Afs_geo%3A101620260,' \
                         # '             sortBy-%3ER,' \
                         # '             resultType-%3EJOBS' \
                         # '             )' \
                         # '&start=25'



    def get_my_class_status(self):
        status = {}
        status['self._keywords'] = self._keywords
        status['self._keywords_ids_info'] = self._keywords_ids_info
        status['self._tot_jobs_num'] = self._tot_jobs_num
        status['self._timePostedRange'] = self._timePostedRange
        status['self._location'] = self._location
        # status['self._extracted_jobs_id'] = self._extracted_jobs_id
        # status['self._jobs_id_list'] = self._jobs_id_list
        # status['self._jobs_id_link_list'] = self._jobs_id_link_list
        # status['self._links_25_jobs_description'] = self._links_25_jobs_description
        # status['self._list_of_jobs_description'] = self._list_of_jobs_description
        # status['self._base_url_to_get_jobs_ids'] = self._base_url_to_get_jobs_ids

        return status

    def _get_headerHandler(self):
        return  self._headerHandler

    def save_jobs_descriptions_to_file(self, file_name_start:str):
        '''
        Dumps data into file. File name composed as follows:
            - {file_name_start} + {DD-MM-YY} . json
        Dumps into  'scraped_files' folder
        :param data:
        :return:
        '''
        datenow = datetime.datetime.now().date().strftime('%Y-%m-%d')
        timenow = datetime.datetime.now().strftime('%d-%m-%Y_%H:%M:%S')
        file_name = 'scraped_files/' + file_name_start + '-' + datenow + '.json'

        with open (file_name, 'w') as fh:
            json.dump(self._list_of_jobs_description, fh)

    def _save_and_change_headerHandler(self, response):
        """
        This method should be used after each request from LinkedIn.
        This method will change 'persons' == wokers who is going to request data from LinkedIn.

        What it does:
        Gets 'response' and updates the current 'headers' and 'headerHandler'.
        Requests the next 'headerHandler' and gets new 'headers'.

        :param response:
        :return:
        """

        # updating headers
        self._headers = self._headerHandler.handle_header_changes_from_response(response)

        # updating headerHandler
        self._headerHandler.set_headers(self._headers)

        # saving headers back to file
        self._headerHandler.save_headers()

        # getting the new headers file
        self._linkedin_header_file = self._headerQ.get_next_header_file()

        # setting the new 'headerHandler'
        self._headerHandler = LinkedInHeaderHandler(
            header_file_name=self._linkedin_header_file)
        # updating current headers
        self._headers = self._headerHandler.get_headers()

    def _get_data_from_scraped_link(self,link_to_scrap:str) -> json:
        """
        Get link to scrap and return scraped data in JSON
        :param link_to_scrap:
        :return:
        """

        sleep_time = random.randint(self._min_sec_sleep_between_requests,self._max_sec_sleep_between_requests)
        # print(f"\t\t\tSleep before scrap: {sleep_time} [sec]\n"
        #       f"\t\t\tScrap url: {link_to_scrap}")
        print(".", end="")
        time.sleep(sleep_time)
        print(f">>> request.get({link_to_scrap})")
        response = requests.get(link_to_scrap, headers=self._headers)
        self._save_and_change_headerHandler(response=response)
        # self._headers = self._headerHandler.handle_header_changes_from_response(response)
        # self._headerHandler.set_headers(self._headers)
        if response.status_code < 400:
            return response.json()
        else:
            print(f"\nResponse code: {response.status_code}")

    def _create_link_to_scrap_jobs_ids(self, start_with:int, keywords:str) -> str:
        """
        Creates a link that will return the list with jobs ids.
        start_with -> start with job number. Usually jumps in 25 {pagination}
        :return:
        """
        # '&filters=List(' \
        # '             timePostedRange-%3Er604800,' \
        # '              locationFallback - % 3EIsrael,'\
        # '             geoUrn-%3Eurn%3Ali%3Afs_geo%3A101620260,' \
        # '             sortBy-%3ER,' \
        # '             resultType-%3EJOBS' \
        # '             )' \
        # '&start=25'
        timePostedRange_str = 'timePostedRange-%3E' + self._timePostedRange + ','
        locationFallback =  'locationFallback-%3E' +urllib.parse.quote(self._location) + ','
        geoUrn_str = 'geoUrn-%3Eurn%3Ali%3Afs_geo%3A' + self._geo_coding[self._location] + ','
        sortBy_str = 'sortBy-%3ER,'
        resultType_str = 'resultType-%3EJOBS)'
        keywords_str ='&keywords='+ urllib.parse.quote(keywords)
        start_str = '&start=' + str(start_with)

        filter_str = '&filters=List(' + timePostedRange_str + locationFallback + geoUrn_str + sortBy_str + resultType_str

        ret_val = self._base_url_to_get_jobs_ids +keywords_str + filter_str + start_str

        return ret_val

    def _get_tot_num_of_jobs_per_keyword(self, keyword: str, data: json) -> int:
        
        # Get number of jobs id from the link if it's for the first time
        if self._keywords_ids_info[keyword]['tot_jobs_num'] is None:
            # Need a lock here for multithreading
            self._keywords_ids_info[keyword]['tot_jobs_num'] = int(data['data']['paging']['total'])
        
        return self._keywords_ids_info[keyword]['tot_jobs_num']

    def _get_start_num_of_jobs_per_keyword(self, keyword: str, data: json) -> int:

        # Get number of jobs id from the link if it's for the first time
        if self._keywords_ids_info[keyword]['start'] is None:
            # Need a lock here for multithreading
            self._keywords_ids_info[keyword]['start'] = int(data['data']['paging']['start'])

        return self._keywords_ids_info[keyword]['start']

    def _create_all_links_to_scrap_ids_per_keyword(self):
        """
        Creates a link and saves to "self._keywords_ids_info" according to keyword
        Creates all possible links with jobs ids inside and append to "self._jobs_id_link_list"
        :return:
        """

        print(f"\n>>> Creating list  of links with ids according keywords")
        for keyword in self._keywords:

            # Create initial link to retrieve tot_jobs_num
            self._keywords_ids_info[keyword]['initial_link'] = self._create_link_to_scrap_jobs_ids(start_with=0,keywords=keyword)

            # Get data (scrap)
            data = self._get_data_from_scraped_link(self._keywords_ids_info[keyword]['initial_link'])

            self._get_start_num_of_jobs_per_keyword(keyword=keyword, data=data)

            # get tot_num_of_jobs per keywords
            tot_jobs_num = self._get_tot_num_of_jobs_per_keyword(keyword=keyword, data=data)
            print(f"\n\t\t Key word = {keyword} , Tot num of jobs = {tot_jobs_num}")

            # Retrieving all ids from initial link
            self._extract_jobs_ids_from_json(data=data)

            # Creates all possible links with jobs ids inside and append to "self._jobs_id_link_list"
            # Starting from 25, since we scrapped the initial link for each keyword
            for start_with in range (25, tot_jobs_num, 25):
                self._jobs_id_link_list.append(self._create_link_to_scrap_jobs_ids(start_with=start_with,keywords=keyword))

        print(f"\n\t\t Jobs id links (each has 25 jobs inside to be scrapped) = {self._jobs_id_link_list}")

    def _extract_jobs_ids_from_json(self, data: json) -> list[str]:
        """
            Get link for the page that represents linkedin jobs. In this link could be maximum 25 ids for jobs.
            Each link has inside information about
                - total number of jobs ids (data -> paging -> total)
                - starting from (data -> paging -> start)
                - number of ids in this link (data -> paging -> count)
            Ids are extracted with regex from:
                - (data -> included -> [i] -> entityUrn)
            The method returns list of ids.

            data :
            :param data: JSON file of the scrapped link to extract ids
            :return:
        """

        # saving scraped file in the file
        # Need a lock for multithreading

        # Get number of jobs ids in this link
        jobs_count = int(data['data']['paging']['count'])
        jobs_tot = int(data['data']['paging']['total'])

        if jobs_count > jobs_tot:
            jobs_count=jobs_tot

        scraped_ids = []
        try:
            for i in range(jobs_count):
                self._extracted_jobs_id +=1
                scraped_ids.append(str(re.findall('\d+', data['included'][i]['entityUrn'])[0]))
        except Exception as e:
            print(f"\nProbably out of range. Trying to scrap numbers that not exist. >>> {e}")

        # Update list of ids in the class
        # Need a lock here for multithreading
        self._jobs_id_list.extend(scraped_ids)
        # self._extracted_jobs_id += jobs_count

        return scraped_ids

    def _extract_jobs_ids_from_all_jsons(self):
        """
        Goes through dictionary of "self._keywords_ids_info" and extracts all Jobs_ids
        :return:
        """

        print(f"\n>>> Go through each link that will return data with max 25 jobs ids\n"
              f">>> Number of links with ids to scrap = {len(self._jobs_id_link_list)}")
        # Go through each link that will return data with max 25 jobs ids
        for url_link_25 in self._jobs_id_link_list:
            json_data = self._get_data_from_scraped_link(link_to_scrap=url_link_25)
            self._extract_jobs_ids_from_json(data=json_data)

    # We have self._jobs_id_list with list of jobs ids to scrapp

    def _get_list_of_jobs_id_without_duplications(self):
        """
        Takes "self._jobs_id_list" and removes duplications
        Updates "self._extracted_jobs_id"
        :return:
        """
        self._jobs_id_list = list(set(self._jobs_id_list))

        # self._jobs_id_list = len(self._jobs_id_list)
        self._tot_jobs_num = len(self._jobs_id_list)
        print(f"\n>>> New jobs posted for the last {self._timePostedRange} = {self._tot_jobs_num}\n")

        return self._jobs_id_list

    def _create_list_links_to_scrap_jobs_descriptions(self, list_of_jobs_ids = None):
        """
        Creates list of links with request for description for 25 jobs positions.
        Returns list of links to be scraped.
        :return:
        """

        # pg_base = "https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.PrefetchJobDetails-103&jobCardPrefetchQuery=(jobUseCase:JOB_DETAILS,prefetchJobPostingCardUrns:List(urn%3Ali%3Afsd_jobPostingCard%3A%283171742204%2CJOB_DETAILS%29,urn%3Ali%3Afsd_jobPostingCard%3A%283167406824%2CJOB_DETAILS%29,urn%3Ali%3Afsd_jobPostingCard%3A%283130723947%2CJOB_DETAILS%29,urn%3Ali%3Afsd_jobPostingCard%3A%283130724692%2CJOB_DETAILS%29,urn%3Ali%3Afsd_jobPostingCard%3A%283130722947%2CJOB_DETAILS%29,urn%3Ali%3Afsd_jobPostingCard%3A%283170356240%2CJOB_DETAILS%29,urn%3Ali%3Afsd_jobPostingCard%3A%283119230212%2CJOB_DETAILS%29))&q=prefetch"
        pg_base = "https://www.linkedin.com/voyager/api/voyagerJobsDashJobCards?decorationId=com.linkedin.voyager.dash.deco.jobs.PrefetchJobDetails-103&jobCardPrefetchQuery=(jobUseCase:JOB_DETAILS,prefetchJobPostingCardUrns:List("
        pg_before_id = "urn%3Ali%3Afsd_jobPostingCard%3A%28"
        pg_after_id = "%2CJOB_DETAILS%29,"
        pg_end = "))&q=prefetch"


        if list_of_jobs_ids == None:
            jobs_ids_no_duplicates = self._get_list_of_jobs_id_without_duplications()
        else:
            jobs_ids_no_duplicates = list_of_jobs_ids

        # Requesting jobs that might already be in the db
        qs_values = Job.objects.filter(source_job_id__in=jobs_ids_no_duplicates,
                                       source__icontains='LinkedIn').values()
        existing_jobs_in_db = []
        for job_exist in qs_values:
            # getting job_ids that exist in db and in the 'jobs_ids_no_duplicates'
            existing_jobs_in_db.append(int(job_exist['source_job_id']))

        # uniq_jobs_ids :  is filtered jobs_ids from duplicates and filtered that does not exist in database
        uniq_jobs_ids = set(jobs_ids_no_duplicates).difference(set(existing_jobs_in_db))

        jobCount = 1

        pg_link = pg_base

        for i, job_id in enumerate(uniq_jobs_ids):
            pg_link = pg_link + pg_before_id + str(job_id) + pg_after_id

            if (jobCount == 25) or (i == len(uniq_jobs_ids)-1):
                pg_link = pg_link[:-1] + pg_end
                self._links_25_jobs_description.append(pg_link)
                pg_link = pg_base
                jobCount = 1
            else:
                jobCount += 1

        return self._links_25_jobs_description

    def _scrap_jobs_description(self):
        """
        Scrapes job descriptions in batches of 25 from LinkedIn
        :return:
        """
        for link_description in self._links_25_jobs_description:
            try:
                job_description_json = self._get_data_from_scraped_link(link_to_scrap=link_description)
                self._list_of_jobs_description.append(job_description_json)
            except Exception as e:
                print("\n",e)

        # Need a lock

    def retrieve_jobs_descriptions_from_linkedin(self):
        """
        Goes through all procedures: scrapes all jobs data and returns 'self._list_of_jobs_description'
        This method should be used only once to retrieve jobs descriptions from linkedIn

        !!!To get a list of already scraped jobs use get_list_of_jobs_description() method

        :return: self._list_of_jobs_description
        """
        self._create_all_links_to_scrap_ids_per_keyword()
        self._extract_jobs_ids_from_all_jsons()
        self._create_list_links_to_scrap_jobs_descriptions()

        print(f"\n>>> Starting to scrap jobs descriptions")
        self._scrap_jobs_description()

        return self._list_of_jobs_description

    def retrieve_jobs_descriptions_from_linkedin_with_jobs_list(self,list_of_jobs_ids ):
        a = self._create_list_links_to_scrap_jobs_descriptions(list_of_jobs_ids=list_of_jobs_ids)
        print(a)
        print(f"\n>>> Starting to scrap jobs descriptions")
        self._scrap_jobs_description()
        return self._list_of_jobs_description

    def get_list_of_jobs_description(self):
        return self._list_of_jobs_description


if __name__ == '__main__':

    jobs_title_search = [
        "android", "ios"

    ]


    linkedin_job_tasker = LinkedInJobsScraper(
        jobs_title_search,
        location='israel',
        timePostedRange='day',
        # linkedin_header_file ='configs/headers_files/linkedin_headers_0.json',
        min_sec_sleep_between_requests = 2,
        max_sec_sleep_between_requests = 6)
    linkedin_job_tasker.retrieve_jobs_descriptions_from_linkedin()
    linkedin_job_tasker.save_jobs_descriptions_to_file(file_name_start="israel_test_2")
    pprint(linkedin_job_tasker.get_my_class_status())





