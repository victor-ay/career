"""
How to use:

    # Create Handler
    headerHandler = HeaderHandler(header_file_name='linkedin_headers_0.json')

    # Requesting data from LinkedIn
    response = request_linkedin(url=url, headers=headerHandler.get_headers())

    # Use "response" (headers, cookies) to update cookies and headers for the next request
    headerHandler.handle_changes_from_response(response)

    # Save / Rewrites json file that holds headers. In this case 'linkedin_headers_0.json'
    headerHandler.save_headers()

"""


import json
import re
from pprint import pprint

import requests

# The url is for internal testing only
# This url requests info for 25 jobs. It's providing 25 jobs ids.
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


# This headers for demonstration only.
# This is how LinkedIn headers looks like
    # headers = {
    #     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36',
    #     'csrf-token': 'ajax:2918111014867513287',
    #     'cookie':
    #     'bcookie="v=2&f73a89e2-296c-470c-8724-91d19e695678"; bscookie="v=1&2022062121132628309a49-e964-42c8-88ec-f6a6d94722e9AQFJqCAIKyye1dN5lYrnhLLbUV4Y-HhQ"; JSESSIONID="ajax:2918111014867513287"; li_theme=light; li_theme_set=app; li_sugr=86e86bdd-e3bf-4e97-bbb4-23024dccfe3b; _gcl_au=1.1.361179661.1655846165; g_state={"i_l":0}; G_ENABLED_IDPS=google; _guid=fee4813e-03bf-4a65-8d27-42d0364e3c81; aam_uuid=30722516814145316542175151343104450939; timezone=Asia/Jerusalem; liap=true; lang=v=2&lang=en-us; li_at=AQEDATRluvgF23xpAAABhol0VksAAAGG2fJqSE0Ang_bloQGEJYWNEkfz17wS4SGx3aUBHLJBYpeifYTSK6sGQYWqrPQKAVvhl9Pxhx2wITjyyqhtyIT5p8gAoYZS6dVjfyOFKWwCZ3TgEQYdtXOUwr5; AnalyticsSyncHistory=AQIU7ltE_NoqHQAAAYa15e14ZDG3-pZnNBMwzpsDfTASUQYPZn_ZIg3ypDYkDqUft8xJhndLSChQC6G-2b73-g; lms_ads=AQF0-6XC4C2hlwAAAYa15e5dMbqmNz8XYjXwPEoPM2dThYSHIx7q_REx2oqPuClbId6xfnFxHD2icWvOQ5mgaK1VYUQyqsAd; lms_analytics=AQF0-6XC4C2hlwAAAYa15e5dMbqmNz8XYjXwPEoPM2dThYSHIx7q_REx2oqPuClbId6xfnFxHD2icWvOQ5mgaK1VYUQyqsAd; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19423%7CMCMID%7C30573763729732222852224953742619742896%7CMCAAMLH-1678693790%7C6%7CMCAAMB-1678693790%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1678096190s%7CNONE%7CvVersion%7C5.1.1%7CMCCIDH%7C1845937615; sdsc=22%3A1%2C1678089003163%7EJAPP%2C0%2BQOPSz6z5f8Cpx0qJtWAf8eO7uI%3D; UserMatchHistory=AQKpuNdHiNuIcAAAAYa1_AM7VzvSvCEJWt6Y9LdTBcn_KHZKInQ6Yi4HtHIOjIkQL2kkDO-d7h3xryvQwCheJ4q-RkJcyCeYXn-zqJfHACEgrIHreuhO0eAneEFy5I2n-Mzs2-hINBLIb_h6CTXp40cAQNiK_3gvdVPnvufENorgL4T0NfMIj1sZ7_hKIxFqyISFwLgR5eFwD1DklHBQCqM2IcjRuiRXB8U7_hAkNLng3OGUTc4IxkqLf3oDHiUK1R9cvsGpVDvILAD1O06GAOgIwkPZh-vN6JPlMZE; lidc="b=VB32:s=V:r=V:a=V:p=V:g=4235:u=92:x=1:i=1678090438:t=1678131538:v=2:sig=AQEzKxilkLnIZrjcnC6_aQrcxFiiNmFb"'
    #
    #         ,
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

def request_linkedin(url, headers):
    """
    Simple request method.
    Provide headers for LinkedIn scrapping
    Returns response from the request

    :param url:
    :param headers:
    :return:
    """
    return requests.get(url=url, headers=headers)

class LinkedInHeaderHandler:
    """
    HeaderHandler is a class to handle changes in headers / cookies for scrapping.

    HeaderHandler is initiated with json file that holds for the initial headers state.
    """

    def __init__(self, header_file_name:str):

        self._header_file_name= header_file_name

        with open(self._header_file_name, 'r') as fh:
            self._headers = json.load(fh)

        self._cookie_str = self._headers["cookie"]
        self._cookie_dictionary = {}
        self._response = None
        self._create_cookie_dict_from_str()

    def __str__(self):
        return f"{self._headers}"

    def __repr__(self):
        return f"{self._headers}"

    def _create_cookie_dict_from_str(self, cookie_str : str =None):
        """
        Get string with all cookies and returns dictionary of cookies
        :param cookie_str:
        :return:
        """
        if cookie_str is None:
            cookie_str = self._cookie_str

        cookie_lst = cookie_str.strip().split('; ')
        for c_elem in cookie_lst:
            splitted = re.split('=', c_elem, maxsplit=1)

            if len(splitted) > 1:
                c_key = splitted[0]
                c_value = splitted[1].strip("'")
                self._cookie_dictionary[c_key] = c_value

        return self._cookie_dictionary

    def _update_cookie_dictionary_from_response(self, response):
        # get response
        # get all protected cookies and update the current "self._cookie_dictionary"

        new_cookies = response.cookies._cookies
        cookie_section = ['.linkedin.com', '.www.linkedin.com']

        # Example of responsed cookie params
        # sdsc = response.cookies._cookies['.linkedin.com']['/']['sdsc'].value
        if len(new_cookies) > 0:
            for cookies_param in self._cookie_dictionary:
                for section in cookie_section:
                    try:
                        param_update = new_cookies.get(section).get('/').get(cookies_param)
                        if param_update is not None:
                            self._cookie_dictionary[cookies_param] = param_update.value
                    except Exception as e:
                        print(e)



        return self._cookie_dictionary

    def _create_cookie_str_from_dict(self) -> str:
        """
        Transforms "self._cookie_dictionary" into string and saves to "self._cookie_str"
        :return:
        """
        cookie_list = []
        for c_elem in self._cookie_dictionary:
            cookie_list.append(c_elem+'='+self._cookie_dictionary[c_elem])
        self._cookie_str =('; ').join(cookie_list)

        return self._cookie_str

    def _update_headers(self):
        """
        Updates "cookies" in headers
        :return:
        """
        self._headers["cookie"] = self._cookie_str
        return self._headers

    def set_headers(self, headers):
        """
        Header setter
        Returns headers structured as dictionary (<self._headers>)

        :param headers:
        :return:
        """
        self._headers = headers
        return self._headers

    def get_headers(self):
        """
        Getter of headers.
        Returns headers structured as dictionary (<self._headers>)

        :return:
        """
        return self._headers

    def save_headers(self):
        """
        Rewrites the initial file that holds headers for the next time usage
        :return:
        """
        with open(self._header_file_name, 'w') as fh:
            json.dump(self._headers, fh)

    def handle_header_changes_from_response(self, response):
        """
        This method receives the < response > from the scrapping request and updates the headers as follows:
         - Gets response cookies and update the current "self._cookie_dictionary"
         - Converts received cookies into string -> Transforms "self._cookie_dictionary" into string and saves to "self._cookie_str"
         - Updates "cookies" in headers

        Returns updated headers dictionary <self._headers>
        :param response:
        :return:
        """
        self._response=response
        self._update_cookie_dictionary_from_response(response=self._response)
        self._create_cookie_str_from_dict()
        self._update_headers()
        return self._headers

if __name__ == '__main__':
    headerHandler = LinkedInHeaderHandler(header_file_name='configs/headers_files/linkedin_headers_0.json')
    response = request_linkedin(url=url, headers=headerHandler.get_headers())

    # Testing HeaderHandler
    for i in range(10):
        print(f">> i = {i}")
        response = request_linkedin(url=url, headers=headerHandler.get_headers())
        print(f"\tResponse status = {response.status_code}")
        headerHandler.handle_header_changes_from_response(response)

    headerHandler.save_headers()


