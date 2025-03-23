import os
import requests
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
from google_auth_oauthlib.flow import InstalledAppFlow

# Load environment variables
load_dotenv()

# SerpApi Configuration
SERPAPI_API_KEY = os.getenv("SERPAPI_API_KEY")
SEARCH_QUERY = "data analysis internship OR junior data analyst remote"

# Google Sheets Configuration
USE_SERVICE_ACCOUNT = os.getenv("USE_SERVICE_ACCOUNT", "true").lower() == "true"
SPREADSHEET_NAME = "Internship Tracker"
WORKSHEET_NAME = "Jobs"

if USE_SERVICE_ACCOUNT:
    SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SHEETS_CREDENTIALS")
    SCOPES = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
else:
    SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive.file"]

def authenticate_google_sheets():
    """Authenticate Google Sheets using OAuth or Service Account"""
    if USE_SERVICE_ACCOUNT:
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
        creds = flow.run_local_server(port=0)
    return gspread.authorize(creds)

def fetch_jobs():
    """Fetch job postings from Google Jobs using SerpApi"""
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_jobs",
        "q": SEARCH_QUERY,
        "hl": "en",
        "location": "Kenya",
        "api_key": SERPAPI_API_KEY
    }
    
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        jobs = response.json().get("jobs_results", [])
        
        return [
            {
                "Title": job["title"],
                "Company": job["company_name"],
                "Location": job.get("location", "Remote"),
                "Posted": job.get("detected_extensions", {}).get("posted_at", "N/A"),
                "Job Link": f"https://www.google.com/search?q={job['title']}+{job['company_name']}+job"
            }
            for job in jobs
        ]
    except requests.exceptions.RequestException as e:
        print(f"Error fetching jobs: {e}")
        print(f"Request URL: {response.url}")
        print(f"Response Content: {response.content}")
        return []
    
def update_google_sheet(jobs):
    """Update Google Sheets with job postings"""
    try:
        creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"])
        client = gspread.authorize(creds)
        
        # List all spreadsheets the service account has access to
        spreadsheets = client.openall()
        print("Spreadsheets accessible by the service account:")
        for spreadsheet in spreadsheets:
            print(f"- {spreadsheet.title}")
        
        # Open the specified spreadsheet
        sheet = client.open(SPREADSHEET_NAME).worksheet(WORKSHEET_NAME)

        print("Connected to Google Sheets ✅")
        print("Clearing sheet...")
        sheet.clear()
        print("Adding headers...")
        headers = ["Title", "Company", "Location", "Posted", "Job Link"]
        sheet.append_row(headers)

        print(f"Adding {len(jobs)} jobs...")
        for job in jobs:
            print("Adding job:", job)
            sheet.append_row(list(job.values()))

        print(f"✅ Updated {len(jobs)} job listings in Google Sheets.")

    except gspread.exceptions.SpreadsheetNotFound as e:
        print(f"❌ Spreadsheet not found: {SPREADSHEET_NAME}")
        print(f"Exception type: {type(e)}")
        print(f"Exception args: {e.args}")
    except Exception as e:
        print(f"❌ Error updating Google Sheets: {e}")
        print(f"Exception type: {type(e)}")
        print(f"Exception args: {e.args}")

if __name__ == "__main__":
    print("Fetching jobs...")
    jobs = fetch_jobs()
    print(f"Found {len(jobs)} jobs.")

    print("Updating Google Sheets...")
    update_google_sheet(jobs)
    print("Update complete!")
    