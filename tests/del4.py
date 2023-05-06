import json
from pprint import pprint

import requests

def changeCookiesInHeaders(headers_old, cookies_new):
    headers_new = headers_old
    headers_new['cookie'] = cookies_new
    return headers_new


def saveHeaders(headers):
    with open('jooble_headers.json', 'w') as fh:
        json.dump(headers,fh)

def loadHeaders():
    with open('jooble_headers.json', 'r') as fh:
        headers = json.load(fh)
    return headers

# cookies ="datadome=32fBbK_19CibZ4DAqmQEJ3jGJidr~fQBcjWdl-iE3NP7LVgayyuOOv3bvvOzb_0gT4VAM8JG9rG4WVOHzVnixFb3CRWZx9TIrNF8gVQR5lST31UlSwqHJsEaTIJHtZWw; Max-Age=31536000; Domain=.jooble.org; Path=/; Secure; SameSite=Lax" \
#          "SessionCookie.us=-5816226222376922004*-5844040110523295946*638179513050805977; Domain=.jooble.org; Path=/; Expires=Tue, 23 Apr 2024 16:41:45 GMT" \
#          "SessionUtmCookie.us=; Domain=.jooble.org; Path=/; Expires=Tue, 23 Apr 2024 16:41:45 GMT" \
#          "user_bucket=4; Path=/; Expires=Fri, 23 Jun 2023 16:41:45 GMT" \
#          "LastVisit=4/24/2023 10:41:45 AM; Path=/; Expires=Sun, 23 Jul 2023 16:41:45 GMT" \
#          "rk_groups=113-0,132-0,498-0; Path=/; Expires=Tue, 23 Apr 2024 16:41:45 GMT" \
#          "sever=40; Path=/; Expires=Sat, 21 Oct 2023 16:41:45 GMT" \
#          ".AspNetCore.Session=CfDJ8BN+kMUDCQNOuWhRq3LeNDBy2FcIl6dUwo8SV7Am6dugUsCFX0/sti0KUcqnAurMjPj+El4yk/FDBiLHci9ZY/M8OIW7Rpg/OcF6G1naxO5SaM2e3mm7veClu46pYtlhh0CSH6rXMetTDYeRmPa4z6iBBNhtAWJjR2M21Zr6iEF3; Path=/; SameSite=Lax"





headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',

    'pragma' : 'no-cache',
    'sec-ch-device-memory' : '8',
    'sec-ch-ua-arch':'"arm"',


    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-encoding': 'gzip, deflate, br',
    'accept-language': 'en-US,en;q=0.9',


    'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
    'sec-ch-ua-full-version-list' : 'Chromium";v="110.0.5481.177", "Not A(Brand";v="24.0.0.0", "Google Chrome";v="110.0.5481.177',
    'sec-ch-ua-model': '""',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': "macOS",
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user' : '?1',
    'upgrade-insecure-requests' : '1'
    }

# headers =loadHeaders()
# headers = changeCookiesInHeaders(headers,cookies)

# headers = loadHeaders()

# url = "https://jooble.org/desc/-1893614387435137868"
# # for i in range(3):
# response = requests.get(url, headers=headers)
# cookies = response.headers._store['set-cookie'][1]
# headers = changeCookiesInHeaders(headers,cookies)
# pprint(response )
#
# saveHeaders(headers)

import requests
# response = requests.get('http://www.dev2qa.com')
response = requests.get('https://jooble.org')
# cookies_jar = response.cookies.RequestsCookieJar()
ck = response.cookies

ck.update()
# n_headers = changeCookiesInHeaders(headers,ck)
# print(ck)
# response = requests.get('https://jooble.org/desc/-1893614387435137868', headers=headers, cookies=ck)
# print(response.cookies)