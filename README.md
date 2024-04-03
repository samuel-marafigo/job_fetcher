
This application fetches job postings from brazilian job posting platforms based on specific search criteria and export the gathered data into Excel files for further analysis.

## Dependencies

To run this application, you will need Python 3.x and the following packages:

- pandas>=1.4.0
- requests>=2.27.0
- openpyxl>=3.0.9

You can install these dependencies by running:

```bash
pip install -r requirements.txt
```

## Structure

The application consists of the following modules:

- `main.py`: The entry point of the application, orchestrating the job fetching and data exporting.
- `gupy.py` and `solides.py`: These modules contain the `GupyJobFetcher` and `SolidesJobFetcher` classes, respectively, which are responsible for fetching job data from the platforms.
- `file_operations.py`: This module includes the `ExcelExporter` class for exporting fetched data to Excel files.

## Usage

1. Ensure all dependencies are installed.
2. Run `main.py` to start the job fetching and data exporting process:

```bash
python main.py
```

This script will fetch job postings according to the specified parameters (which are in the code), and export the data to Excel files with the following naming pattern: 'platform name'_'current date'.xlsx

## Notes

- This application currently filters job openings based on hard-coded parameters. The parameters are displayed while the script is being executed and can be altered in the `main.py` file.
