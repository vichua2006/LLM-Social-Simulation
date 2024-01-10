from googleapiclient.discovery import build
from google.oauth2.service_account import Credentials

# Define the scope and credentials for Google Sheets API
SCOPES = ['https://www.googleapis.com/auth/spreadsheets.readonly']
SERVICE_ACCOUNT_FILE = 'path/to/your/credentials.json'  # Replace with your JSON file path

# The ID of your spreadsheet
SPREADSHEET_ID = '1cGVFdxYCkTnGMqdb2dv5JJsRw7VeJRZAam3UmnaAMcs'

def get_prompts_from_sheet(range_name):
    credentials = Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    service = build('sheets', 'v4', credentials=credentials)

    # Call the Sheets API
    sheet = service.spreadsheets()
    result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range=range_name).execute()
    values = result.get('values', [])

    if not values:
        print('No data found.')
    else:
        return values

# Example: Read data from a specific range
range_name = 'Sheet1!A1:E5'  # Adjust the range and sheet name as necessary
prompts = get_prompts_from_sheet(range_name)

# Example usage
print(prompts)
