from gupy import GupyJobFetcher
from solides import SolidesJobFetcher
from file_operations import ExcelExporter

def main():
    gupy_job_fetcher = GupyJobFetcher()
    solides_job_fetcher = SolidesJobFetcher()
    exporter = ExcelExporter()

    # Define the list of search parameters
    search_parameters = [
        {"job_name": "desenvolvedor", "city": "Curitiba", "state": "Paraná", "today_only": True},
        {"job_name": "desenvolvedor", "city": "São José dos Pinhais", "state": "Paraná", "today_only": True},
        {"job_name": "estagiario", "city": "Curitiba", "state": "Paraná", "today_only": True},
        {"job_name": "estagiario", "city": "São José dos Pinhais", "state": "Paraná", "today_only": True},
        {"job_name": "estagiario", "workplaceType": "remote", "today_only": True},
        {"job_name": "estagio", "workplaceType": "remote", "today_only": True},
        {"job_name": "junior", "city": "Curitiba", "state": "Paraná", "today_only": True},
        {"job_name": "junior", "city": "São José dos Pinhais", "state": "Paraná", "today_only": True},
        {"job_name": "qa", "workplaceType": "remote", "today_only": True},
        {"job_name": "python", "workplaceType": "remote", "today_only": True},
        {"job_name": "full stack", "workplaceType": "remote", "today_only": True},
        {"job_name": "back end", "workplaceType": "remote", "today_only": True}
    ]

    # Iterate over the search parameters and make the calls
    for index, params in enumerate(search_parameters, start=1):
        print(f"Calling {search_parameters[index]}:")
        solides_result = solides_job_fetcher.callApi(**params)
        gupy_result = gupy_job_fetcher.callApi(**params)
        print(solides_result)
        print(gupy_result)
        exporter.save_to_excel(solides_result, 'solides')
        exporter.save_to_excel(gupy_result, 'gupy')
        print()

if __name__ == "__main__":
    main()