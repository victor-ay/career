from pathlib import Path
import json
from pprint import pprint

import requests

def changeCookiesInHeaders(headers_old, cookies_new):
    headers_new = headers_old
    headers_new['cookie'] = cookies_new
    return headers_new

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',

    'pragma' : 'no-cache',

    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',
    'cache-control' : 'no-cache',
    'referer':'https://il.indeed.com/?r=us',

    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-full-version-list' : 'Chromium";v="110.0.5481.177", "Not A(Brand";v="24.0.0.0", "Google Chrome";v="110.0.5481.177',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "macOS",
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user' : '?1',
    'upgrade-insecure-requests' : '1',
    'Connection': 'keep-alive'

    }

cookies = {
    'jaSerpCount':'2',
    'indeed_rcc' : '"LV:CTK:UD"',
    'ac' : 'jjw0oOOmEe2IZMUw/bqdMQ#jjyCwOOmEe2IZMUw/bqdMQ',
    '_gid': 'GA1.2.159883723.1682453665',
    '_gcl_au':'1.1.583015424.1682453665',
    '_ga':'GA1.2.1241930391.1682453665',
    '_cfuvid':'IPDqo5k07gIEQUHJh4MyH7AmFTsDYtoNKBOYxDFxbP8-1682453660516-0-604800000',
    '__cf_bm':'Qz_k5cPOlOleIUX8T.Jxxwx7cUY_fuksanIWdJkOmyo-1682453660-0-ATWn0yO27qAf/MNdTNWSYYus/QiONvpeZmLX+05wH2rLDlTcIO+EkLM+L+ogSMhHnIMoKqPEiNdt0MVpG+HuCmo=',
    'UD':'"LA=1682455973:CV=1682453664:TS=1682453664:SG=f60cf3ab9fdd223e0214d24f18ef5062"',
    'SURF':'kXNW7xJDbBRqxebmU731Oc9knH7w6016',
    'RQ':'"q=software+engineer&l=&ts=1682455973821"',
    'PPID':'""',
    'MICRO_CONTENT_CSRF_TOKEN':'ae1lObFvEkOWAzN5Bd07SrktjQu4DIVn',
    'LV':'"LA=1682453664:CV=1682453664:TS=1682453664"',
    'LOCALE': 'en',
    'JSESSIONID': 'F90377FFD1EDD8440F55FEF001829FA7',
    'INDEED_CSRF_TOKEN': 'jRz5pbFCGYWXp4oAn2S3IY2zJqShDe9V',
    'CTK': '1gut0r0p6j6dj800',
    'CSRF': 'qFYNSmpNYi3lwxQBxRSsmUR0ZkHqAqSx',
    'mdserp':'""'

}

url = 'https://il.indeed.com/hp/log/homepageModules?logType=shown&tk=1gut6dvaii9ba800&clientSideTk=1gut6dvaii9ba800187ba66fff11&moduleName=feedTabs&itemNames'


response = requests.get(url,headers=headers)
ck = response.cookies
pprint(response)
pprint(response.text)
pprint(ck)

