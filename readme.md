# Projeto de Acesso Restrito a Arquivos no Google Drive via Web App Flask

Este projeto desenvolve uma aplicação web que permite acesso a arquivos e pastas no Google Drive com diferentes níveis de permissão para usuários distintos. A autenticação é realizada através do Google OAuth 2.0, e o armazenamento de dados de usuários e permissões é feito em um banco de dados SQL.

## Descrição

A aplicação permite aos usuários logar-se utilizando suas contas do Google. Após a autenticação, o sistema exibe uma dashboard com as pastas e arquivos aos quais o usuário tem permissão de acesso.  O sistema implementa controle fino sobre as permissões, permitindo diferentes níveis de acesso (leitura, escrita, etc.) para cada arquivo/pasta.

## Estrutura do Projeto
content_copy
Use code with caution.
Markdown

projeto_drive_acesso/
├── app/
│ ├── init.py
│ ├── models.py # Modelos SQL
│ ├── routes.py # Rotas e endpoints
│ ├── forms.py # Formulários
│ ├── google_drive_api.py # Funções para interação com a API do Google Drive
│ ├── database.py # Funções de conexão e manipulação do banco de dados
│ └── static/
│ └── style.css
├── templates/
│ ├── base.html # Template base da aplicação
│ ├── login.html # Formulário de login
│ ├── dashboard.html # Dashboard de arquivos/pastas
│ └── access_denied.html
├── requirements.txt
├── run.py
└── config.py # Configurações (credenciais do Google, banco de dados, etc.)

## Pré-requisitos

* Python 3.x
* Flask framework
* SQLAlchemy (ORM para banco de dados)
* `google-api-python-client`
* oauth2client
* (Opcional, mas recomendado) Werkzeug
* (Opcional, mas recomendado) WTForms para formulários

## Instalação

1. Clone o repositório:
   ```bash
   git clone <repositório>
content_copy
Use code with caution.

Crie um ambiente virtual (recomendado):

python3 -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate (Windows)
content_copy
Use code with caution.
Bash

Instale as dependências:

pip install -r requirements.txt
content_copy
Use code with caution.
Bash

Criar e configurar o Projeto no Google Cloud Platform:

Crie um projeto no Google Cloud Platform.

Configure as credenciais do Google Cloud em config.py (incluindo o Client ID, Client Secret, etc.).

Configurar o banco de dados:

Configure a conexão com o banco de dados em config.py.

Execute o script de migração alembic upgrade head (se estiver utilizando Alembic).

Uso

Execute a aplicação:

python run.py
content_copy
Use code with caution.
Bash

Acesse a aplicação no seu navegador.

Considerações Importantes

Segurança: Este projeto requer o armazenamento seguro das credenciais do Google e do banco de dados (utilizando variáveis de ambiente).

Escalabilidade: O projeto foi projetado para aplicações web, e considera a estrutura para expandir as funcionalidades conforme necessário.

Documentação: A documentação foi fornecida para facilitar o entendimento e desenvolvimento do projeto. Aprofunde a documentação em cada componente do código.

Teste Unitário: Adicionar testes unitários para componentes críticos do projeto (como a API do Google Drive e a lógica de permissões) irá aumentar a confiabilidade.

Contribuições

Contribuições são bem-vindas! Por favor, abra um issue ou um pull request para reportar problemas ou adicionar funcionalidades.

content_copy
Use code with caution.