from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey, create_engine, text
from sqlalchemy.future import engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from werkzeug.security import generate_password_hash, check_password_hash
import os

db = SQLAlchemy()  # Cria a instância do SQLAlchemy

# Função para criar as tabelas
def create_tables(app):
    Base = declarative_base()  # Cria a base para declaração

    class User(Base):
        __tablename__ = 'users'
        id = Column(Integer, primary_key=True)
        email = Column(String, unique=True, nullable=False)
        password = Column(String, nullable=False)


        def __repr__(self):
            return f"<User {self.email}>"



    class File(Base):
        __tablename__ = 'files'
        id = Column(Integer, primary_key=True)
        name = Column(String, nullable=False)
        path = Column(String, nullable=False)
        size = Column(Integer, nullable=False)
        user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
        user = relationship('User', backref='files')


        def __repr__(self):
          return f"<File {self.name}>"



    # Inicializa a conexão com o banco de dados
    Base.metadata.create_all(app=app) # Utiliza o contexto do app

# ... (outras classes e funções de modelo, como funções para
# obter usuários ou arquivos, etc.)


# Esta função (se necessário) é para recuperar a sessão do banco de dados
def get_db():
    db = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return db()

# Se você precisar de um método para criar o banco de dados
# def create_database():
#     db.create_all(app=app) # Usa a função create_all adequada


# ... (código para criar o banco de dados ou outra lógica)
class User:
    pass


class File:
    pass