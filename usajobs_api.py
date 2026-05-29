import requests
from utils.config import USAJOBS_API_KEY

def fetchusa_jobs(keyword, location="remote", results_per_page=5):
    """
    Fetches job listings from the USAJOBS Search API and returns a cleaned, structured list.
    """
    if not USAJOBS_API_KEY:
        print("❌ Error: USAJOBS_API_KEY is missing. Cannot fetch jobs.")
        return []

    # USAJOBS requires Host, User-Agent, and Authorization-Key exactly like this
    headers = {
        "Host": "data.usajobs.gov",
        "User-Agent": "gauravkumarixc@gmail.com",
        "Authorization-Key": USAJOBS_API_KEY
    }

    # API keys are strictly case-sensitive: ResultsPerPage instead of results_per_page
    params = {
        "Keyword": keyword,
        "ResultsPerPage": str(results_per_page)
    }

    # Handle location/remote filters based on USAJOBS API specifications
    if location.lower() == "remote":
        params["RemoteIndicator"] = "True"
    else:
        params["LocationName"] = location

    url = "https://data.usajobs.gov/api/search"

    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        
        if response.status_code == 200:
            raw_results = response.json().get('SearchResult', {}).get('SearchResultItems', [])
            return parse_jobs_data(raw_results)
        else:
            print(f"❌ Error fetching jobs from USAJOBS: {response.status_code}")
            print(f"Response: {response.text}")
            return []
            
    except requests.exceptions.RequestException as e:
        print(f"❌ Network error while connecting to USAJOBS API: {e}")
        return []

def parse_jobs_data(job_items):
    """
    Helper function to parse and clean the highly nested USAJOBS API response
    into a clean list of dictionaries for your agents to easily digest.
    """
    parsed_jobs = []
    
    for item in job_items:
        matched_obj = item.get('MatchedObjectDescriptor', {})
        
        # Safely extract specific elements required by jd_analyst and resume_cl_agent
        job_details = {
            "id": matched_obj.get("PositionID"),
            "title": matched_obj.get("PositionTitle"),
            "agency": matched_obj.get("OrganizationName"),
            "department": matched_obj.get("DepartmentName"),
            "url": matched_obj.get("PositionURI"),
            "location": ", ".join([loc.get("LocationName") for loc in matched_obj.get("PositionLocation", []) if loc.get("LocationName")]),
            "summary": matched_obj.get("UserArea", {}).get("Details", {}).get("JobSummary", ""),
            "duties": "\n".join(matched_obj.get("UserArea", {}).get("Details", {}).get("MajorDuties", [])),
            "qualifications": matched_obj.get("QualificationSummary", "")
        }
        
        # If the direct summary/duties paths are blank, fallback safely to generalized descriptions
        if not job_details["summary"]:
            job_details["summary"] = matched_obj.get("PositionDescription", [{}])[0].get("Body", "")[:500]

        parsed_jobs.append(job_details)
        
    return parsed_jobs