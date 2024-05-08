class Query:
    def __init__(self, job_name):
        self.job_name = job_name

    def get_queries(self):
        return [
            {"job_name": self.job_name, "city": "Curitiba", "state": "Paraná", "today_only": False},
            {"job_name": self.job_name, "city": "São José dos Pinhais", "state": "Paraná", "today_only": False},
            {"job_name": self.job_name, "workplaceType": "remote", "today_only": False}
        ]
