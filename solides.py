import requests
from datetime import datetime

class SolidesJobFetcher:

    def __map_workplace_type(self, workplaceType):
        """
        Maps English workplace type values to Portuguese translations. Needed for this specific API.

        Args:
            workplaceType (str): The type of workplace.

        Returns:
            str: Portuguese translation of the workplace type.
        """
        type_mapping = {
            "on-site": "presencial",
            "hybrid": "hibrido",
            "remote": "remoto"
        }
        return type_mapping.get(workplaceType, workplaceType)

    def fetch_jobs_data(self, job_name, cities=None, state=None, workplaceType=None):
        """
        Fetches job data from the Solides API.

        Args:
            job_name (str): The name of the job to search for.
            cities (str, optional): The cities where the job is located, separated by commas. Defaults to None.
            state (str, optional): The state where the job is located. Defaults to None.
            workplaceType (str, optional): Possible arguments: presencial, hibrido, remoto. Defaults to None.

        Returns:
            list: A list of dictionaries containing the fetched job data.
        """
        url = "https://apigw.solides.com.br/jobs/v3/portal-vacancies-new"
        params = {
            "page": 1,
            "title": job_name,
            "take": 20
        }
        locations = []
        if cities and state:
            state_abbreviation = {"Paraná": "PR"}.get(state, state)
            locations = [f"{city.strip()} - {state_abbreviation}" for city in cities.split(",")]
        if locations:
            params["locations"] = ' '.join(locations)
        if workplaceType is not None:
            params["jobsType"] = self.__map_workplace_type(workplaceType)

        response = requests.get(url, params=params)

        if response.status_code == 200:
            response_data = response.json().get("data", {})
            job_items = response_data.get("data", []) 
            return job_items
        else:
            print(f"Failed to fetch data. Status code: {response.status_code}")
            return None


    def __filter_job_data(self, jobs_data, today_only=False):
        """
        Filters the fetched job data.

        Args:
            jobs_data (list): List of dictionaries containing the fetched job data.
            today_only (bool, optional): Flag to filter jobs that were published today only. Defaults to False.

        Returns:
            list: A list of dictionaries containing the filtered job data.
        """
        filtered_data = []
        today_date = datetime.today().strftime('%Y-%m-%d')
        
        for job in jobs_data:
            if today_only:
                if self.__parse_published_date(job.get("createdAt")) == today_date:
                    filtered_data.append(self.__extract_job_info(job))
            else:
                filtered_data.append(self.__extract_job_info(job))
    
        return filtered_data

    def __extract_job_info(self, job):
        """
        Extracts relevant job information from a job data dictionary.

        Args:
            job (dict): Dictionary containing job data.

        Returns:
            dict: Dictionary containing relevant job information.
        """
        return {
            "name": job.get("title"),
            "careerPageName": job.get("companyName"),
            "publishedDate": self.__parse_published_date(job.get("createdAt")),
            "workplaceType": job.get("jobType"),
            "city": job.get("city", {}).get("name") if job.get("city") is not None else None, #solides may return no city or state
            "state": job.get("state", {}).get("name") if job.get("city") is not None else None,
            "jobUrl": job.get("redirectLink")
        }

    def __parse_published_date(self, published_date_str):
        """
        Parses the published date string and extracts only the date part.

        Args:
            published_date_str (str): String containing the published date.

        Returns:
            str: Extracted date part of the published date string.
        """
        if published_date_str:
            return published_date_str.split("T")[0]

    def callApi(self, job_name, city=None, state=None, workplaceType=None, today_only=False):
        """
        Orchestrates the workflow by fetching and filtering job data.

        Args:
            job_name (str): The name of the job to search for.
            city (str, optional): The city where the job is located. Defaults to None.
            state (str, optional): The state where the job is located. Defaults to None.
            workplaceType (str, optional): The type of workplace for the job. Defaults to None.
            today_only (bool, optional): Flag to filter jobs that were published today only. Defaults to False.

        Returns:
            list or str: A list of dictionaries containing the filtered job data if jobs are found,
                         otherwise a message indicating no jobs were found.
        """
        jobs_data = self.fetch_jobs_data(job_name, city, state, workplaceType)
    
        if jobs_data:
            return self.__filter_job_data(jobs_data, today_only)


       

