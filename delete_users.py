import csv
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
# We need the 'user' scope to delete accounts
SCOPES = ['https://www.googleapis.com/auth/admin.directory.user']

def main():
    creds = None
    # The file token.json stores the user's access and refresh tokens
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('admin', 'directory_v1', credentials=creds)

        # Path to your uploaded CSV file
        csv_file_path = 'To Delete - 31st Jan.csv'
        
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            print(f"Starting deletion process for users in {csv_file_path}...")
            
        # Edit below to match your CSV column name for email addresses
            for row in reader:
                email = row['Email Address']
                try:
                    # The actual delete command
                    service.users().delete(userKey=email).execute()
                    print(f"Successfully deleted: {email}")
                except HttpError as error:
                    if error.resp.status == 404:
                        print(f"Skip: {email} not found (might already be deleted).")
                    else:
                        print(f"Error deleting {email}: {error}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
    