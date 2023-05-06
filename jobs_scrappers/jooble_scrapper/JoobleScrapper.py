
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

class JoobleScrapper():
    def __init__(self, titles: list):
        self._titles = titles
        self._date = str # Format yyyy-mm-dd
        self._tot_results = None
        self._max_results_per_request = 100 # Returns 76 results max
        self._dict_of_jobs = dict() # key = id , value = job_card
        self._list_of_jobs_id = []

    def get_jobs_data(self, days_posted: int):
        # requests all passible combinations according to titles
        # days_posted : number of days when the job was posted
        # returns dict_of_jobs
        pass

    def get_list_of_jobs_ids(self):
        return self._list_of_jobs_id

    def get_job_description(self,job_id:str):
        # requests additional info and updates info in the dict_of_jobs.
        # the additional info will be : isRemoteJob, content (description), isShiftJob, datePosted, awayData -> (domain, link)
        pass


