from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
import os

# Configurações do banco de dados (substitua com seu próprio banco de dados)
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///db.sqlite3')

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Modelo para usuário
class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    # Adicione outros atributos do usuário, como nome, data de cadastro, etc.
    permissions = relationship("Permission", back_populates="user", cascade="all, delete-orphan")


# Modelo para permissões (cada usuário pode ter várias permissões)
class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    # ... Outros campos para definir a permissão (leitura, escrita, etc)
    # Exemplo:
    arquivo_ou_pasta = Column(String, nullable=False) # Nome do arquivo ou pasta
    tipo_acesso = Column(String, nullable=False)  # Ex: 'leitura', 'escrita'


# Modelo para arquivo no Google Drive
class GoogleDriveFile(Base):
    __tablename__ = 'google_drive_files'
    id = Column(Integer, primary_key=True)
    nome_arquivo = Column(String, unique=True, nullable=False)
    caminho = Column(String, nullable=False)
    tipo_permissao_id = Column(Integer, ForeignKey('permissions.id')) #Associa o tipo de permissão
    permissao = relationship("Permission", back_populates="google_drive_file", uselist=False, cascade='all,delete-orphan')


# Associa o relacionamento "user" ao "permission"
Permission.user = relationship("User", back_populates="permissions")

# Associa a "permissao" a um arquivo do Google Drive
Permission.google_drive_file = relationship("GoogleDriveFile", back_populates="permissao")


def create_db_and_tables():
    Base.metadata.create_all(engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Exemplo de uso (apenas para demonstração)
# if __name__ == "__main__":
#     from sqlalchemy import create_engine
#     engine = create_engine(DATABASE_URL)
#     Base.metadata.create_all(engine)  # Cria tabelas no banco se elas não existirem.