import os
from dotenv import load_dotenv

load_dotenv()

# Configurações da aplicação
PROJECT_NAME = "MeuAplicativoDrive"
SECRET_KEY = os.getenv('SECRET_KEY')
GOOGLE_DRIVE_CLIENT_ID = os.getenv('GOOGLE_DRIVE_CLIENT_ID')
GOOGLE_DRIVE_CLIENT_SECRET = os.getenv('GOOGLE_DRIVE_CLIENT_SECRET')
GOOGLE_DRIVE_REFRESH_TOKEN = os.getenv('GOOGLE_DRIVE_REFRESH_TOKEN')
DATABASE_URL = os.getenv("DATABASE_URL")


# Configurações do banco de dados (adapte conforme necessário)
SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///database.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configurações da API do Google Drive (substitua pelos seus valores)
SCOPES = ['https://www.googleapis.com/auth/drive']

# Configurações adicionais
UPLOAD_FOLDER = os.path.join('uploads') #Pasta para uploads temporários
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'} #Tipos de arquivos permitidos