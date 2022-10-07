from __future__ import print_function
import os.path
import time
import io
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import sqlite3

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']


def job_gmail():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credenciales.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    
    a=[]

    try:
        service = build('gmail', 'v1', credentials=creds)
        resultado = service.users().messages().list(userId = 'me', labelIds= ['INBOX']).execute()
        messages = resultado.get('messages',[])
        for message in messages:
            msg = service.users().messages().get(userId = 'me', id=message['id'], format = 'full').execute()
            data = msg['payload']['headers']
            for values in data:
                name = values['name']
                if name == "From":
                    from_name = values['value']
                    a.append("From : "+from_name)
                if name == "Subject":
                    subject = values['value']
                    a.append("Asunto : "+subject)
                if name == "Date":
                    date = values['value']
                    a.append("Fecha : "+str(date))
            data = msg['payload']['parts']
            for values in data:
                name = values['body']['data']
                a.append(name)
    
    except HttpError as error:
        print(f'An error occurred: {error}')
    
    conexion = sqlite3.connect("C:\Users\Brayan\Desktop\ejemplo\prueba\db.sqlite3")
    try:
        conexion.execute("insert into Email value(?,?,?,?)",(a[0],a[1],a[2],a[3]))
        conexion.commit()
    except sqlite3.OperationalError:
        print("Problema")
    conexion.close()