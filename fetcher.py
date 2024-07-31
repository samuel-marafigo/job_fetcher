from query import Query  # Import the custom Query class
from gupy import GupyJobFetcher
from solides import SolidesJobFetcher
from file_operations import ExcelExporter
import os
from datetime import datetime
import asyncio
from multiprocessing import Process, Queue

def fetcher(job_title, queue):
    gupy_job_fetcher = GupyJobFetcher()
    solides_job_fetcher = SolidesJobFetcher()
    exporter = ExcelExporter()
    
    query_instance = Query(job_title)
    search_parameters = query_instance.get_queries()

    mergedResults = []

    # Iterate over each dictionary in the list
    for current_query_dict in search_parameters:
        job_name = current_query_dict['job_name']
      
        solides_result = solides_job_fetcher.callApi(**current_query_dict)
        gupy_result = gupy_job_fetcher.callApi(**current_query_dict)

        mergedResults.extend(solides_result)
        mergedResults.extend(gupy_result)

        for result in solides_result:
            publish_date = datetime.strptime(result["publishedDate"], '%Y-%m-%d').date()
            folder_path = f"./Found jobs/Solides/{publish_date}"
            os.makedirs(folder_path, exist_ok=True)
            filename = f"{folder_path}/solides_{job_name}_{publish_date}.csv"
            exporter.save_to_csv([result], filename)
            

        for result in gupy_result:
            publish_date = datetime.strptime(result["publishedDate"], '%Y-%m-%d').date()
            folder_path = f"./Found jobs/Gupy/{publish_date}"
            os.makedirs(folder_path, exist_ok=True)
            filename = f"{folder_path}/gupy_{job_name}_{publish_date}.csv"
            exporter.save_to_csv([result], filename)

    queue.put(mergedResults)

async def fetcherResult(job_titles):
    processes = []
    queue = Queue()
    
    for job in job_titles:
        process = Process(target=fetcher, args=(job, queue))
        processes.append(process)
        process.start()

    for process in processes:
        process.join()

    all_merged_results = []
    while not queue.empty():
        results = queue.get()
        all_merged_results.extend(results)
    
    return all_merged_results

  