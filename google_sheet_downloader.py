import gspread
from oauth2client.service_account import ServiceAccountCredentials
import csv
import os
project_directory = os.path.dirname(os.path.abspath(__file__))
# Set the path to your credentials JSON file (downloaded from the Google Developers Console)
credentials_path = os.path.join(project_directory, 'env/fine-blueprint-383621-f496d5563f81.json')
# URL of the Google Sheet you want to read
spreadsheet_url = 'https://docs.google.com/spreadsheets/d/1cGVFdxYCkTnGMqdb2dv5JJsRw7VeJRZAam3UmnaAMcs/edit#gid=0'
# Local path where you want to save the CSV file
csv_file_path = os.path.join(project_directory, 'Data/prompt_sheet.csv')

def download_google_sheet_to_csv():
    download_google_sheet_to_csv(credentials_path, spreadsheet_url, csv_file_path)

def download_google_sheet_to_csv(credentials_path, spreadsheet_url, local_file_name):
    # Initialize the scope and credentials
    scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    credentials = ServiceAccountCredentials.from_json_keyfile_name(credentials_path, scope)
    gc = gspread.authorize(credentials)

    # Extract the spreadsheet ID from the URL
    spreadsheet_id = spreadsheet_url.split('/d/')[1].split('/edit')[0]

    # Open the Google Sheet by its ID and get all values
    worksheet = gc.open_by_key(spreadsheet_id).sheet1  # Change 'sheet1' to the name of your specific sheet
    values = worksheet.get_all_values()

    # Write values to a local CSV file
    with open(local_file_name, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerows(values)

def read_local_csv():
    if not os.path.exists(csv_file_path):
        download_google_sheet_to_csv(credentials_path, spreadsheet_url, csv_file_path)
        print(f"sheet not exist, Downloaded the Google Sheet to {csv_file_path}")
    # Read the local CSV file
    with open(csv_file_path, mode='r', newline='', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        return list(reader)

if __name__ == "__main__":
    try:
        # Download the Google Sheet to a local CSV file
        download_google_sheet_to_csv()
        
        # Read the local CSV file
        sheet_data = read_local_csv()
        
        # Print the data from the local CSV file
        for row in sheet_data:
            print(row)
    
    except Exception as e:
        print(f"An error occurred: {str(e)}")
