import os
from datetime import datetime
import pandas as pd

class ExcelExporter:
    def __init__(self):
        pass

    def save_to_excel(self, data, file_name_prefix):
        """
        Saves the data to an Excel file, appending to it if it already exists, unless there are no valid data to save.

        Args:
            data (list): A list of dictionaries containing the data to be saved.
            file_name_prefix (str): The prefix for the Excel file name.

        Returns:
            str: The name of the saved Excel file or a message indicating no data was saved.
        """
        # Check if data is empty, None, or contains a specific message indicating no values to add
        if not data or data in [
            "Nenhuma vaga encontrada com os critérios selecionados",
            "Falha ao buscar os dados das vagas"
        ]:
            return "No valid data to save. Operation skipped."

        today_date = datetime.today().strftime('%Y-%m-%d')
        file_name = f"{file_name_prefix}_{today_date}.xlsx"
        new_df = pd.DataFrame(data)

        if os.path.exists(file_name):
            existing_df = pd.read_excel(file_name)
            combined_df = pd.concat([existing_df, new_df], ignore_index=True).drop_duplicates(keep='first')
        else:
            combined_df = new_df

        combined_df.to_excel(file_name, index=False)
        return f"Data saved to '{file_name}' successfully."
