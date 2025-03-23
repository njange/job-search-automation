# Job Search Automation

This project automates the process of searching for job postings and updating a Google Sheets spreadsheet with the results. It uses the SerpApi to fetch job postings from Google Jobs and the Google Sheets API to update the spreadsheet.

## Prerequisites

- Python 3.6 or higher
- A Google Cloud project with the Google Sheets API enabled
- A SerpApi account and API key

## Setup

1. **Clone the repository:**

    ```sh
    git clone https://github.com/njange/job-search-automation.git
    cd job-search-automation
    ```

2. **Create a virtual environment and activate it:**

    ```sh
    python3 -m venv venv
    source venv/bin/activate
    ```

3. **Install the required packages:**

    ```sh
    pip install -r requirements.txt
    ```

4. **Set up environment variables:**

    Create a `.env` file in the project directory with the following content:

    ```env
    SERPAPI_API_KEY=your_serpapi_api_key
    GOOGLE_SHEETS_CREDENTIALS=path_to_your_service_account_json_file
    ```

    Replace `your_serpapi_api_key` with your actual SerpApi API key and `path_to_your_service_account_json_file` with the path to your Google service account JSON file.

5. **Configure Google Sheets:**

    - Create a Google Sheets spreadsheet and name it (e.g., "Internship Tracker").
    - Share the spreadsheet with the service account email found in your JSON credentials file (e.g., `your-service-account@your-project.iam.gserviceaccount.com`).
    - Create a worksheet within the spreadsheet and name it (e.g., "Jobs").

6. **Update the configuration in [jobs.py](http://_vscodecontentref_/0):**

    Ensure the following variables are set correctly in [jobs.py](http://_vscodecontentref_/1):

    ```python
    SPREADSHEET_NAME = "Internship Tracker"
    WORKSHEET_NAME = "Jobs"
    ```

## Usage

1. **Run the script:**

    ```sh
    python3 jobs.py
    ```

    The script will fetch job postings based on the search query and update the specified Google Sheets spreadsheet with the results.

## Customization

- **Search Query:**

    Update the [SEARCH_QUERY](http://_vscodecontentref_/2) variable in [jobs.py](http://_vscodecontentref_/3) to customize the job search query:

    ```python
    SEARCH_QUERY = "your_custom_search_query"
    ```

- **Location:**

    Update the `location` parameter in the [fetch_jobs](http://_vscodecontentref_/4) function to change the job search location:

    ```python
    params = {
        "engine": "google_jobs",
        "q": SEARCH_QUERY,
        "hl": "en",
        "location": "your_location",
        "api_key": SERPAPI_API_KEY
    }
    ```

## Troubleshooting

- **ModuleNotFoundError:**

    Ensure all required packages are installed by running:

    ```sh
    pip install -r requirements.txt
    ```

- **Spreadsheet or Worksheet Not Found:**

    Ensure the spreadsheet and worksheet names are correct and that the service account has access to the spreadsheet.

## License

This project is licensed under the MIT License. See the LICENSE file for details.