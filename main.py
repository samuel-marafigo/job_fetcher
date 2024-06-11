from query import Query  # Import the custom Query class
from gupy import GupyJobFetcher
from solides import SolidesJobFetcher
from file_operations import ExcelExporter
import os
from datetime import datetime
from multiprocessing import Process, Event

def main(job_title):
    gupy_job_fetcher = GupyJobFetcher()
    solides_job_fetcher = SolidesJobFetcher()
    exporter = ExcelExporter()
    
    query_instance = Query(job_title)
    search_parameters = query_instance.get_queries()

    # Iterate over each dictionary in the list
    for current_query_dict in search_parameters:
        job_name = current_query_dict['job_name']
        print(f"Calling API for job: {job_name}")
        try:
            solides_result = solides_job_fetcher.callApi(**current_query_dict)
            gupy_result = gupy_job_fetcher.callApi(**current_query_dict)

            for result in solides_result:
                publish_date = datetime.strptime(result['publishedDate'], '%Y-%m-%d').date()
                folder_path = f"./Found jobs/Solides/{publish_date}"
                os.makedirs(folder_path, exist_ok=True)
                filename = f"{folder_path}/solides_{job_name}_{publish_date}.csv"
                exporter.save_to_csv([result], filename)

            for result in gupy_result:
                publish_date = datetime.strptime(result['publishedDate'], '%Y-%m-%d').date()
                folder_path = f"./Found jobs/Gupy/{publish_date}"
                os.makedirs(folder_path, exist_ok=True)
                filename = f"{folder_path}/gupy_{job_name}_{publish_date}.csv"
                exporter.save_to_csv([result], filename)

        except TypeError as e:
            print(f"Error in API call for {job_name}: {str(e)}")
        print()

if __name__ == "__main__":
    job_titles = ["estagiario", "estagio", "junior", "desenvolvedor", "developer", "java", "python", "react",
                  "backend", "fullstack", "intern", "suporte", "support"
                  ]

    processes = []

    for job in job_titles:
        processes.append(Process(target=main, args=(job,)))

    for process in processes:
        process.start()
  