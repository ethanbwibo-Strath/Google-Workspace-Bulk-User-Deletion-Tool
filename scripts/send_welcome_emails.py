import base64
import csv
import os
import mimetypes
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build


SCOPES = [
    'https://www.googleapis.com/auth/admin.directory.user',
    'https://www.googleapis.com/auth/admin.directory.group.member',
    'https://www.googleapis.com/auth/gmail.send'
]

def create_message_with_attachment(to, subject, html_content, file_path=None):
    message = MIMEMultipart()
    message['to'] = to
    message['from'] = 'me'
    message['subject'] = subject

    message.attach(MIMEText(html_content, 'html'))

    if file_path and os.path.exists(file_path):
        content_type, encoding = mimetypes.guess_type(file_path)
        if content_type is None:
            content_type = 'application/octet-stream'
        main_type, sub_type = content_type.split('/', 1)
        
        with open(file_path, 'rb') as f:
            part = MIMEBase(main_type, sub_type)
            part.set_payload(f.read())
            
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', 'attachment', filename=os.path.basename(file_path))
        message.attach(part)

    raw = base64.urlsafe_b64encode(message.as_bytes())
    return {'raw': raw.decode()}

def main():
    creds = None
    # Simple paths: looks in the current working directory
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

    # Simple path to template
    with open('templates/welcome_email_template.html', 'r') as f:
        template = f.read()

    # Simple path to CSV
    with open('new_users.csv', mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            personalized_html = template.replace('{{name}}', row['Name']) \
                                         .replace('{{email}}', row['Email']) \
                                         .replace('{{password}}', row['TemporaryPassword'])

            # If you have an attachment, put the filename here (e.g., 'handbook.pdf')
            msg = create_message_with_attachment(
                row['Email'], 
                'Welcome to Missions of Hope International', 
                personalized_html,
                file_path= 'assets\\I.T. Policy 2020 - MOHI.pdf',
                
            )
            
            try:
                service.users().messages().send(userId='me', body=msg).execute()
                print(f"✅ Success: Welcome email sent to {row['Email']}")
            except Exception as e:
                print(f"❌ Error sending to {row['Email']}: {e}")

if __name__ == '__main__':
    main()