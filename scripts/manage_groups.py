import csv
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    'https://www.googleapis.com/auth/admin.directory.user',         # For Deletions
    'https://www.googleapis.com/auth/admin.directory.group.member', # For Groups
    'https://www.googleapis.com/auth/gmail.send'                    # For Onboarding Emails
]

def main():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
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

        # Path to your group management CSV
        csv_file_path = 'group_additions.csv'
        
        with open(csv_file_path, mode='r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            
            for row in reader:
                user_email = row['Email']
                group_email = row['Group']
                
                member_data = {
                    'email': user_email,
                    'role': 'MEMBER'
                }
                
                try:
                    # The command to add a member to a group
                    service.members().insert(groupKey=group_email, body=member_data).execute()
                    print(f"Successfully added {user_email} to {group_email}")
                except HttpError as error:
                    if error.resp.status == 409:
                        print(f"Skip: {user_email} is already a member of {group_email}")
                    else:
                        print(f"Error adding {user_email} to {group_email}: {error}")

    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()