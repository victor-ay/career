from pprint import pprint

import requests

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
    'csrf-token': 'ajax:2918111014867513287',
    'cookie':
    'bcookie="v=2&f73a89e2-296c-470c-8724-91d19e695678"; bscookie="v=1&2022062121132628309a49-e964-42c8-88ec-f6a6d94722e9AQFJqCAIKyye1dN5lYrnhLLbUV4Y-HhQ"; JSESSIONID="ajax:2918111014867513287"; li_theme=light; li_theme_set=app; li_sugr=86e86bdd-e3bf-4e97-bbb4-23024dccfe3b; _gcl_au=1.1.361179661.1655846165; g_state={"i_l":0}; G_ENABLED_IDPS=google; _guid=fee4813e-03bf-4a65-8d27-42d0364e3c81; aam_uuid=30722516814145316542175151343104450939; timezone=Asia/Jerusalem; liap=true; lang=v=2&lang=en-us; li_at=AQEDATRluvgCAMxXAAABhv5b4CMAAAGHZhw6_E0AUPKsWcExkl8XDdHrvsH90qS0Q4I_Vd1ZGr3ufEopXKQTLj1cINAJKkgco8sGiMSWPD6yIgI65jb9JLnhBjQBqB5qVOsOnuw3MvW510vXX6XIff98; AnalyticsSyncHistory=AQJb1-C1yUh7eQAAAYdCD7zFysA73lwHQQyYEwcwDeHSydLGwYExEDFfp3C6neoERwShwc8DZzly0eztMbL7Bg; lms_ads=AQH5kX9p6EaQzQAAAYdCD73j10Oh6E3jPbNPaQTmxvkABeSp0UikFiRb5N2aNnT89Gcxdm_XARQepVZK9VVjnIds9pcOM3hz; lms_analytics=AQH5kX9p6EaQzQAAAYdCD73j10Oh6E3jPbNPaQTmxvkABeSp0UikFiRb5N2aNnT89Gcxdm_XARQepVZK9VVjnIds9pcOM3hz; AMCVS_14215E3D5995C57C0A495C55%40AdobeOrg=1; sdsc=1%3A1SZM1shxDNbLt36wZwCgPgvN58iw%3D; AMCV_14215E3D5995C57C0A495C55%40AdobeOrg=-637568504%7CMCIDTS%7C19450%7CMCMID%7C30573763729732222852224953742619742896%7CMCAAMLH-1681061404%7C6%7CMCAAMB-1681061404%7C6G1ynYcLPuiQxYZrsz_pkqfLG9yMXBpb2zX5dvJdYQJzPXImdj0y%7CMCOPTOUT-1680463804s%7CNONE%7CvVersion%7C5.1.1%7CMCCIDH%7C1845937615; UserMatchHistory=AQLZiuBDs7XTSQAAAYdDR_mYYidqt77hzFb7mpjSmFQZKZ_dJgw3Kla8ab70F0luukow4YIUhv8VCo2YAUJ5XeS1sBsAkGStbj3-DE2-u9ojmpr2R6TlqOycJT_gtHaIWhRZLnnj2Uf4jRLEjyEYyEv0uKslITzvoIIm5GbvGRS3QyDL1gQYsumnCnW5JurpYN38pcf9c2HY56tag8dKtYjjYKoGaYUq8VK1XoKn-qL-qzdVe4M3FyM-3Mf-HSCUO2tTnnlBZlNzzDuSdWbl1Tdl7mkTEWxUfBK_kPs; lidc="b=VB32:s=V:r=V:a=V:p=V:g=4278:u=102:x=1:i=1680461004:t=1680526938:v=2:sig=AQH3-g9h8UhlDUKHNuOeb6Sz0kCe_uPV"'
        ,
    'authority': 'www.linkedin.com',
    'accept': 'application/vnd.linkedin.normalized+json+2.1',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'referer': 'https://www.linkedin.com/jobs/search/?currentJobId=3090136770&geoId=101620260',
    'sec-ch-ua': '" Not A;Brand";v="99", "Chromium";v="102", "Google Chrome";v="102"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "macOS",
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


url = "https://www.linkedin.com/voyager/api/graphql?variables=(start:20,origin:OTHER,query:(flagshipSearchIntent:SEARCH_SRP,queryParameters:List((key:resultType,value:List(COMPANIES))),includeFiltersInResponse:false))&&queryId=voyagerSearchDashClusters.181547298141ca2c72182b748713641b"
data = requests.get(url ,headers=headers)
pprint(data.text)

# print("HCLTech \u00b7 Troy, MI (On-site)")

# import proxyscrape
# collector = proxyscrape.create_collector('my-collector', 'https')  # Create a collector for http resources
# proxy = collector.get_proxy({'country': 'france'})  # Retrieve a united states proxy
# print(proxy) # print the proxy
