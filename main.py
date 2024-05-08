from query import Query  # Import the custom Query class
from gupy import GupyJobFetcher
from solides import SolidesJobFetcher
from file_operations import ExcelExporter

def main():
    gupy_job_fetcher = GupyJobFetcher()
    solides_job_fetcher = SolidesJobFetcher()
    exporter = ExcelExporter()

    # List of job titles you want to search
    job_titles = ["farmaceutico", "estagiario", "estagio", "junior", "desenvolvedor", "developer"]

    # Iterate over each job title and fetch queries for each
    for job_title in job_titles:
        query_instance = Query(job_title)
        search_parameters = query_instance.get_queries()

        # Iterate over each dictionary in the list
        for current_query_dict in search_parameters:
            job_name = current_query_dict['job_name']
            print(f"Calling API for job: {job_name}")
            try:
                solides_result = solides_job_fetcher.callApi(**current_query_dict)
                gupy_result = gupy_job_fetcher.callApi(**current_query_dict)
                print(solides_result)
                print(gupy_result)
                # Optionally save results to Excel
                exporter.save_to_excel(solides_result, 'solides_' + job_name)
                exporter.save_to_excel(gupy_result, 'gupy_' + job_name)
            except TypeError as e:
                print(f"Error in API call for {job_name}: {str(e)}")
            print()

if __name__ == "__main__":
    main()
