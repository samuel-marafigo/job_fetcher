import requests
from datetime import datetime

class GupyJobFetcher:


    def fetch_jobs_data(self, job_name, city=None, state=None, workplaceType=None):
        """
        Fetches job data from the Gupy API.

        Args:
            job_name (str): The name of the job to search for.
            city (str, optional): The city where the job is located. Defaults to None.
            state (str, optional): The state where the job is located. Defaults to None.
            workplaceType (str, optional): Possible arguments: on-site, hybrid, remote. Defaults to None.

        Returns:
            list: A list of dictionaries containing the fetched job data.
        """
        url = "https://portal.api.gupy.io/api/v1/jobs"
        params = {
            "jobName": job_name
        }

        if city is not None:
            params["city"] = city
        if state is not None:
            params["state"] = state
        if workplaceType is not None:
            params["workplaceType"] = workplaceType

        response = requests.get(url, params=params)

        if response.status_code == 200:
            return response.json().get("data", [])
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
                if self.__parse_published_date(job.get("publishedDate")) == today_date:
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
            "name": job.get("name"),
            "careerPageName": job.get("careerPageName"),
            "publishedDate": self.__parse_published_date(job.get("publishedDate")),
            "workplaceType": job.get("workplaceType"),
            "city": job.get("city"),
            "state": job.get("state"),
            "jobUrl": job.get("jobUrl")
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
        else:
            return None

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
            filtered_jobs_data = self.__filter_job_data(jobs_data, today_only)
            if filtered_jobs_data:
                return filtered_jobs_data
            else:
                return "Nenhuma vaga encontrada com os critérios selecionados"
        else:
            return "Falha ao buscar os dados das vagas"


# # Example usage:
# job_fetcher = GupyJobFetcher()
# job_name = "desenvolvedor"
# city = "Curitiba,São José dos Pinhais"
# state = "Paraná"
# workplaceType = "hybrid"
# filtered_jobs_data = job_fetcher.callApi(job_name, city, state, workplaceType, today_only=False)
#
# print(filtered_jobs_data)