from dotenv import load_dotenv
import os
import requests

# Load environment variables from .env file
load_dotenv()

def load_financial_info(ticker):
    """
    Load financial information for a given company from the SEC API.

    Args:
        ticker (str): The stock ticker symbol of the company.

    Returns:
        dict: A dictionary containing the financial information, or None if the request fails.
    """
    user_agent_email = os.getenv("USER_AGENT_EMAIL")
    if not user_agent_email:
        raise ValueError("USER_AGENT_EMAIL is not set in the environment variables.")

    base_url = "https://data.sec.gov/api/xbrl/companyfacts/CIK"
    headers = {
        "User-Agent": f"Financial-RAG 1.0 ({user_agent_email})",
        "Accept": "application/json",
    }

    try:
        # First, get the CIK number for the company
        cik_search_url = f"https://www.sec.gov/files/company_tickers.json"
        response = requests.get(cik_search_url, headers=headers)
        
        if response.status_code != 200:
            print(f"Failed to fetch CIK data: {response.status_code} - {response.reason}")
            return None
            
        companies = response.json()
        cik = None
        
        # Find the CIK for the given ticker
        for entry in companies.values():
            if entry['ticker'].upper() == ticker.upper():
                cik = str(entry['cik_str']).zfill(10)
                break
                
        if not cik:
            print(f"Could not find CIK for ticker {ticker}")
            return None

        # Now get the company facts using the CIK
        url = f"{base_url}{cik}.json"
        print(f"Fetching data from: {url}")  # Debug print
        response = requests.get(url, headers=headers)

        # Check if the request was successful
        if response.status_code == 200:
            return response.json()
        else:
            print(f"Failed to fetch data: {response.status_code} - {response.reason}")
            return None
    except requests.RequestException as e:
        print(f"An error occurred while fetching data: {e}")
        return None

if __name__ == "__main__":
    ticker = "AAPL"  # Apple stock ticker
    try:
        financial_info = load_financial_info(ticker)
        if financial_info:
            print("Financial information for Apple:")
            print(financial_info)
        else:
            print("Failed to retrieve financial information for Apple.")
    except ValueError as e:
        print(e)