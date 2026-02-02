import base64
import csv
import os.path
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Scopes for Gmail Send
SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def main():
    creds = None
    # Load or generate token.json
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

    service = build('gmail', 'v1', credentials=creds)

    # Load the template
    with open('templates/welcome_email_template.html', 'r') as f:
        template = f.read()

    # Process CSV
    with open('new_users.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Replace placeholders
            personalized_html = template.replace('{{name}}', row['Name']) \
                                         .replace('{{email}}', row['Email']) \
                                         .replace('{{password}}', row['TemporaryPassword'])

            # Build the email
            message = MIMEText(personalized_html, 'html')
            message['to'] = row['Email']
            message['from'] = 'me'
            message['subject'] = 'Welcome to Missions of Hope International'
            
            # Encode for Gmail API
            raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
            
            try:
                service.users().messages().send(userId='me', body={'raw': raw_message}).execute()
                print(f"Welcome email sent to: {row['Email']}")
            except Exception as e:
                print(f"Error sending to {row['Email']}: {e}")

if __name__ == '__main__':
    main()