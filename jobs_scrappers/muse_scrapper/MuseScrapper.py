import datetime
import json
import os.path
from asyncio import sleep
from collections import namedtuple
from pprint import pprint
import random
from urllib.parse import urlunparse, urlencode
from bs4 import BeautifulSoup

import requests


class MuseScrapper():
    # Website: https://www.themuse.com/
    # Jobs located: USA + Remote

    def __init__(self, titles:[str], locations:[str] = []):
        self._min_sleep = 2
        self._max_sleep = 7 #seconds
        self._base_jobs_list_url = 'https://www.themuse.com'
        self._date = 'last_7d' # last_7d, last_14d, last_30d
        self._jobs_per_request = 20 # Api requires
        self._timeout_request = 5000 # Api requires
        self._titeles = titles
        self._locations = locations # location is passed as longitude and latitude
        self._initial_urls = {} # {key = title, value = initial_url}
        # Includes urls according to : title, date, location (currently all locations)

        self._last_cursor_per_title = {} # key = title, value={'cursor' : #some cursor , 'is_last' : false}
        self._jobs = {} # key = job_id , value = job_card
        self._jobs_num_returned = None
        self._jobs_num_requested = None

        self._initialize_last_cursor_dictionary()
        self._create_all_initial_urls()


    def _initialize_last_cursor_dictionary(self):
        for title in self._titeles:
            self._last_cursor_per_title[title] = {}
            self._last_cursor_per_title[title]['cursor'] = ''
            self._last_cursor_per_title[title]['is_last'] = False

    def _create_all_initial_urls(self):
        # This will run in init
        Components = namedtuple(
            typename='Components',
            field_names=['scheme', 'netloc', 'url', 'path', 'query', 'fragment']
        )

        for title in self._titeles:
            query_params = {
                'ctsEnabled': 'false',
                'preference': 'selunfnqnpq',
                'limit': self._jobs_per_request,
                'timeout': self._timeout_request,
                'query': title
            }

            # Adding cursor if exists
            if self._last_cursor_per_title[title]['cursor'] != '':
                query_params['start_after'] = self._last_cursor_per_title[title]['cursor']

            nurl = urlunparse(
                Components(
                    scheme='https',
                    netloc='www.themuse.com',
                    query=urlencode(query_params),
                    path='',
                    url='/api/search-renderer/jobs',
                    fragment=''
                )
            )
            self._initial_urls[title] = nurl

        return self._initial_urls

    def scrapp_jobs_from_url(self, url:str, title:str):
        # Requests the list of jobs from Muse
        # and ads info to te self._jobs
        # and returns the dictionary of results as is

        response = requests.get(url=url)
        if len(response.json()["hits"]) == 0:
            self._last_cursor_per_title[title]['is_last'] = True
        else:
            for hit in response.json()["hits"]:
                if hit['score']<30 :
                    self._last_cursor_per_title[title]['is_last'] = True
                    break

                # Add to jobs if not exists
                elif hit['hit']['id'] not in self._jobs:
                    self._jobs[hit['hit']['id']] = hit
                    self._last_cursor_per_title[title]['cursor'] = hit['cursor']
        return self._jobs

    def _get_next_url_per_title(self,title):
        return self._initial_urls[title]+'&start_after='+self._last_cursor_per_title[title]['cursor']

    def store_results_in_file(self):
        file_name = 'muse'+datetime.datetime.now().strftime('%Y-%M-%d_%H-%m-%s')+'.json'
        with open(file_name, 'w') as fh:
            json.dump(self._jobs,fh)

    def scrapp_all_jobs(self, max_num):
        for title, url in self._initial_urls.items():
            url_to_scrap = url
            while (self._last_cursor_per_title[title]['is_last'] == False) and len(self._jobs)<max_num:
                self.scrapp_jobs_from_url(url=url_to_scrap, title=title)
                url_to_scrap = self._get_next_url_per_title(title=title)
                sleep(random.randint(self._min_sleep,self._max_sleep))
        self.store_results_in_file()
        return self._jobs

    def get_job_description(self,short_name,short_title):
        # short_name : is representatyion of company name
        # short_title :  is a representation of the job_id
        path = os.path.join(self._base_jobs_list_url,'jobs',short_name,short_title)
        response = requests.get(path)
        soup = BeautifulSoup(response.content, 'html.parser')
        json_data = json.loads(soup.find('script', {'id': 'JobPost-JSON'}).getText())
        return json_data

if __name__ == '__main__':
    titles = ["software engineer"]
    myMuse = MuseScrapper(titles=titles)
    # response = myMuse.scrapp_all_jobs(max_num=10)
    response = myMuse.get_job_description(short_name='eaton' , short_title='sustaining-electrical-engineer-7f616a')
    pprint(response)


    soup = BeautifulSoup(response.content, 'html.parser')
    json_data = json.loads(soup.find('script',{'id': 'JobPost-JSON'}).getText())
    pprint(json_data)
