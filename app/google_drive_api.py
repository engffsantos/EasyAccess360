# app/google_drive_api.py

from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
import os
import json
import io

# Configurações (substitua pelos seus valores)
SCOPES = ['https://www.googleapis.com/auth/drive']
DRIVE_SERVICE = None  # Inicializa como None, será definido posteriormente


def setup_drive_api():
    """Configura a API do Google Drive."""
    global DRIVE_SERVICE
    creds = None

    # Verifica se há credenciais salvas
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    # Se as credenciais não estiverem válidas ou não existirem
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Salva as credenciais
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    DRIVE_SERVICE = build('drive', 'v3', credentials=creds)


def upload_file_to_drive(file_path, file_name):
    """Carrega um arquivo local para o Google Drive."""
    setup_drive_api()  # Garante que a API esteja configurada
    media = MediaIoBaseUpload(
        io.BytesIO(open(file_path, 'rb').read()),
        mimetype='application/octet-stream'  # ou o tipo correto do arquivo
    )
    try:
        file_metadata = {'name': file_name}
        file = DRIVE_SERVICE.files().create(
            body=file_metadata,
            media_body=media,
            fields='id'
        ).execute()
        return file.get('id')
    except Exception as e:
        print(f"Erro ao carregar o arquivo: {e}")
        return None


def download_file_from_drive(file_id, destination_path):
    """Faz o download de um arquivo do Google Drive."""
    setup_drive_api()  # Garante que a API esteja configurada
    try:
        request = DRIVE_SERVICE.files().get_media(fileId=file_id)
        fh = io.FileIO(destination_path, 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()
            print(f'Download {int(status.progress() * 100)}%')
        return True
    except Exception as e:
        print(f"Erro ao baixar o arquivo: {e}")
        return False

# ... (Outras funções para lidar com permissões, listar arquivos, etc.)

from googleapiclient.http import MediaIoBaseUpload, MediaIoBaseDownload