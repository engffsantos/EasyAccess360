import os
from flask import Flask, render_template, redirect, url_for, flash, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm
from dotenv import load_dotenv
from app.google_drive_api import setup_drive_api, upload_file_to_drive, download_file_from_drive
from werkzeug.utils import secure_filename

# Carrega as variáveis de ambiente
load_dotenv()

# Inicializa o Flask
app = Flask(__name__)

# Configurações do aplicativo (incluindo a chave secreta)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'  # Pasta para uploads

# Inicializa o SQLAlchemy
db = SQLAlchemy(app)


# Configura o LoginManager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Função de carregamento de usuário para o login
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None

# importa os modelos
from app.models import User

# ... (restante do código)

# def allowed_file(filename):
#     ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
#     return '.' in filename and \
#            filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            flash('Email ou senha inválidos.', 'danger')
    return render_template('login.html', form=form)


# ... (outras rotas)

# Função para o upload de arquivos
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if 'file' not in request.files:
        flash('Nenhum arquivo selecionado.', 'danger')
        return redirect(url_for('upload_file'))

    file = request.files['file']
    if file.filename == '':
        flash('Nenhum arquivo selecionado.', 'danger')
        return redirect(url_for('upload_file'))

    # ... (Validação de arquivo)
    # if file and allowed_file(file.filename):
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
    flash('Arquivo enviado com sucesso!', 'success')
    return redirect(url_for('dashboard'))


# ... (outras rotas, incluindo dashboard e logout)

if __name__ == '__main__':
    setup_drive_api()  # Inicia a API do Google Drive
    app.run(debug=True)