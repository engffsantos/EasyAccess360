import os
from flask import Flask, render_template, redirect, url_for, flash, send_from_directory, request
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegisterForm
from dotenv import load_dotenv
from werkzeug.utils import secure_filename
import uuid
from app.models import create_tables, User, File, get_db # Importando a função create_tables

# Carrega as variáveis de ambiente
load_dotenv()

app = Flask(__name__)

# Configurações do aplicativo
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'uploads'


db = SQLAlchemy(app) # Inicializa o SQLAlchemy com a aplicação Flask


login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(int(user_id))
    except:
        return None


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


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='pbkdf2:sha256', salt_length=8)
        new_user = User(email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Usuário registrado com sucesso!', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


@app.route('/dashboard')
@login_required
def dashboard():
    db_session = get_db()
    user_files = db_session.query(File).filter(File.user_id == current_user.id).all()
    db_session.close()
    return render_template('dashboard.html', user_files=user_files)




@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            new_file = File(name=filename, path=os.path.join(app.config['UPLOAD_FOLDER'], filename), size=file.tell(), user_id=current_user.id) # Salvando o arquivo.
            db.session.add(new_file)
            db.session.commit()
            flash('Arquivo enviado com sucesso!', 'success')
            return redirect(url_for('dashboard'))
    return render_template('upload.html')


if __name__ == '__main__':
    create_tables(app) # Criando as tabelas aqui.
    app.run(debug=True)