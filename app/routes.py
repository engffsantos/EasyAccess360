# app/routes.py

from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_user, logout_user, login_required, current_user
from . import models, forms
# from google.oauth2 import id_token
# from google.auth.transport import requests
# from google.cloud import storage

# Importe as classes do seu módulo de modelos (models.py)
# ... substitua pelas suas classes reais
from .models import User
# ... outros imports


# Inicialize um Blueprint
bp = Blueprint('routes', __name__)


@bp.route('/', methods=['GET'])
def index():
    if current_user.is_authenticated:
        return render_template('dashboard.html')
    else:
        return render_template('login.html')


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Lógica de autenticação do Google
        # ... (código para obter dados do formulário de login e autenticar com a API do Google)
        # Exemplo simplificado (substituir com a lógica correta)
        email = request.form.get('email')
        if email:
            user = User.query.filter_by(email=email).first()
            if user:
                login_user(user)
                return redirect(url_for('routes.index'))
            else:
                return "Usuário não encontrado."
        else:
            return "Informe um email."  # ou uma mensagem mais amigável
    return render_template('login.html')


@bp.route('/logout')
@login_required  # Protege a rota
def logout():
    logout_user()
    return redirect(url_for('routes.index'))

# Rotas para exibir arquivos, pastas, etc.

@bp.route('/dashboard')
@login_required
def dashboard():
  #Lógica para buscar arquivos/pastas e mostrar na página
  return render_template('dashboard.html', files=files_list) #Exemplo com lista de arquivos