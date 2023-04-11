# from pprint import pprint
#
# import requests
#
# indeed_url = 'https://il.indeed.com/viewjob?viewtype=embedded&jk=6fb43868eaf37115&from=tp-semfirstjob&tk=1gsl5kbv6kjic800&continueUrl=%2Fjobs%3Fq%3Dsoftware%26from%3DsearchOnHP%26l%3DTel%2BAviv-Jaffa%252C%2B%25D7%259E%25D7%2597%25D7%2595%25D7%2596%2B%25D7%25AA%25D7%259C%2B%25D7%2590%25D7%2591%25D7%2599%25D7%2591&spa=1&hidecmpheader=0'
#
# edu = 'https://edulabs.co.il/'
#
# indeed_2 = 'https://il.indeed.com/jobs?q=software&l=Tel+Aviv-Jaffa%2C+%D7%9E%D7%97%D7%95%D7%96+%D7%AA%D7%9C+%D7%90%D7%91%D7%99%D7%91&start=10&pp=gQAPAAABhypaMAEAAAAB_fPvgQArAQABigvRyodwpTq_MaxHaeGAm8NBiEqElJLhblSmn_CUG25E6N7dhaCPKAAA'
#
# headers = {
#     'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/110.0.0.0 Safari/537.36',
#     'cookie': 'indeed_rcc=CTK; CTK=1gq4oej9bm9d4801; RF="cSKTH5STSNDi6XwjtXXX-e3EaW9MXv2cNRpn5fR2czIHjKe56NmKYU-BlyDwdRl-QBT88d_oVfs="; _mkto_trk=id:699-SXJ-715&token:_mch-indeed.com-1679852625028-23196; SURF=pDmStioqC3njZVTjfz82K7cWiSbrgL6i; __ssid=4333401b9547efa179fc4e13aa84bda; CSRF=RhyRIiqsNiTAa2AjyKkGav481R35wFKC; INDEED_CSRF_TOKEN=xSbiz5HOpQVD2jR2nqscbUshRlD69SFz; _gcl_au=1.1.1977236801.1679853178; SHARED_INDEED_CSRF_TOKEN=xSbiz5HOpQVD2jR2nqscbUshRlD69SFz; LOCALE=en; MICRO_CONTENT_CSRF_TOKEN=5NsmDPOn99uWgyTysByskNsxxRbmZiP0; PPID=""; ROJC=2b685f5fd10d8827; RJAS=v2b685f5fd10d8827; RCLK=jk=a707abe16b3288e6&tk=1gsfhlvnrp5mk800&from=web&rd=VwIPTVJ1cTn5AN7Q-tSqGRXGNe2wB2UYx73qSczFnGU&qd=RnZhMybXSk4M3QtTVGXWodiRfZXjdgfdHWaRxaOFnFsVU3nL9ODrFZtpuajgZ0-lnLsKGJl6H5LfGsUZUwe3s-vMIiAS58CLmqI-0ivjWGrzubNaRheqOlc4aC_-G0UiU_FDyBMEpMoSS89fWFWUQcPZVMASYjjFvsL_1fW45k7qZGXyeKI8ZSjgbEWBYkqi0b97xGnmfqqqEZ2-yvx7Yw&ts=1679854075643&sal=0; _ga_7TCG2YPZJD=GS1.1.1679897251.2.0.1679897251.0.0.0; _cfuvid=Y6ijnN8hgRn4lXd8YyFOrzttUe9dLEIGo8z5wD0jYyY-1679897252885-0-604800000; LOCALE=en; _ga=GA1.2.1357884416.1677344592; _gid=GA1.2.160553603.1680041569; LC="co=IL"; gonetap=1; g_state={"i_p":1680127976635,"i_l":2}; LV="LA=1680041843:LV=1679853176:CV=1680041699:TS=1679853165"; __cf_bm=DlMnTaWcSNNXAc5dr7oq4VPozQ._8_Eu8VGcOmUOTW4-1680042626-0-AWCORMFOs36IIx7dAqBdg26o5BZ+vpwiR8CuPzMma24z+NdLpddEc28Zft27JRMCzBUsHRK3/tWDumxB/pxvpww=; indeed_rcc="PREF:LV:CTK:UD"; PREF="TM=1680042754486:L=Tel+Aviv-Jaffa%2C+%D7%9E%D7%97%D7%95%D7%96+%D7%AA%D7%9C+%D7%90%D7%91%D7%99%D7%91"; jaSerpCount=17; UD="LA=1680042766:CV=1680041698:TS=1680041698:SG=86be040b6335d843663b5f7c04156ca3"; RQ="q=software&l=Tel+Aviv-Jaffa%2C+%D7%9E%D7%97%D7%95%D7%96+%D7%AA%D7%9C+%D7%90%D7%91%D7%99%D7%91&ts=1680042766337:q=software&l=israel&ts=1680042625904:q=software+engineer&l=Tel+Aviv-Jaffa%2C+%D7%9E%D7%97%D7%95%D7%96+%D7%AA%D7%9C+%D7%90%D7%91%D7%99%D7%91&ts=1679854804103:q=&l=%D7%AA%D7%9C+%D7%90%D7%91%D7%99%D7%91+-%D7%99%D7%A4%D7%95%2C+%D7%9E%D7%97%D7%95%D7%96+%D7%AA%D7%9C+%D7%90%D7%91%D7%99%D7%91&ts=1679853176823"; JSESSIONID=C6A0075ADE810FA4158F11EC58F03498; _gat=1; ac=iC76EM24Ee20v42q+/iJQQ#iC9IMM24Ee20v42q+/iJQQ',
#
#     'pragma' : 'no-cache',
#     'referer' : 'https://il.indeed.com/jobs?q=software&l=Tel%20Aviv-Jaffa%2C%20%D7%9E%D7%97%D7%95%D7%96%20%D7%AA%D7%9C%20%D7%90%D7%91%D7%99%D7%91&from=searchOnHP',
#
#     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#     'sec-ch-ua': '"Chromium";v="110", "Not A(Brand";v="24", "Google Chrome";v="110"',
#     'sec-fetch-site' : 'same-origin',
#     'sec-fetch-user' : '?1',
#     'upgrade-insecure-requests': '1',
#     'sec-fetch-mode' : 'navigate',
#     'sec-fetch-dest' : 'document',
#     'sec-ch-ua-platform' : '"macOS"',
#     'sec-ch-ua-mobile' : '?0',
#     'accept-encoding' : 'gzip, deflate, br',
#     # ':scheme' : 'https'
#     }
#
# response = requests.get('https://il.indeed.com/jobs?q=software')
# pprint(response.status_code)

import http.client
from pprint import pprint

host = 'jooble.org'
key = '918c4c20-79ae-4260-8127-22c7c98f204b'

connection = http.client.HTTPConnection(host)
#request headers
headers = {"Content-type": "application/json"}
#json query
body = '{ "keywords": "software engineer"}'
connection.request('POST','/api/' + key, body, headers)
response = connection.getresponse()
print(response.status, response.reason)
print(response.read())