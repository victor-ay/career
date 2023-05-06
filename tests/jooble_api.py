import http.client

# Here is a full list of data you can pass through the code:
# keywords - keywords to search for jobs by;
# location - location to search for jobs in;
# radius (optional) - radius for search (will be converted to km) type:string
# salary (optional) - minimum salary for search type: integer
# page (optional) - to get jobs on the specified page of the SERP;
# ResultOnPage (optional) - number of jobs to be displayed on a page;
# datecreatedfrom (optional) - to get jobs created after this date. format: yyyy-mm-dd
# companysearch (optional):
# -true - to search for keywords in company name of jobs, not in job title or description;
# -false - to search for keywords in job title or description
import json
from pprint import pprint

import requests

host = 'jooble.org'
key = '918c4c20-79ae-4260-8127-22c7c98f204b'

connection = http.client.HTTPConnection(host)
#request headers
headers = {"Content-type": "application/json"}
#json query
body = '{ "keywords": "software engineer", "location": "California", "datecreatedfrom": "2023-04-20", "page":2}'
# body = '{ "keywords": "software engineer", "location": "usa", "page":10, , "ResultOnPage" : "100"}'

connection.request('POST','/api/' + key, body, headers)
response = connection.getresponse()
print(response.status, response.reason)
# pprint(response.read().decode('utf-8'))

jooble_d = json.loads(response.read().decode('utf-8'))

# pprint(jooble_d['jobs'][0]['id'])
pprint(jooble_d)




# headers = {"Content-type": "application/json"}
# url = host + '/api/'
# body = { "keywords": "software engineer", "location": "usa"}
# data = requests.post(url,data=body, auth={'key':key} ,headers=headers)
# pprint(data.text)