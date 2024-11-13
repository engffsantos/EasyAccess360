import os
from flask import Flask, render_template, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import db, User, File  # Importe os modelos
from app.forms import LoginForm, RegisterForm
import uuid
from dotenv import load_dotenv
from app.google_drive_api import setup_drive_api, upload_file_to_drive, download_file_from_drive  # Importando a API

load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'  # Substitua por uma chave secreta forte
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')  # Use variável de ambiente
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Rotas
# ... (restante do código)

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
    user_files = File.query.filter_by(user_id=current_user.id).all()
    return render_template('dashboard.html', user_files=user_files)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/download_file/<int:file_id>')
@login_required
def download_file(file_id):
    # ... (lógica para encontrar o arquivo pelo file_id)
    # Substitua o código abaixo com a lógica de busca
    file = File.query.get_or_404(file_id)
    if file.user_id == current_user.id:  # Verifica permissão
        return send_file(file.path, as_attachment=True)  # Baixando o arquivo.
    else:
        flash("Erro ao baixar o arquivo.", "danger")
        return redirect(url_for('dashboard'))


if __name__ == '__main__':
    app.run(debug=True)