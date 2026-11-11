import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexão com o PostgreSQL (utilizadores e credenciais do docker-compose)
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql://postgres:postgres@localhost:5432/minierp"
)

# Cria o motor de conexão
engine = create_engine(DATABASE_URL)

# Cria a fábrica de sessões para interagir com o banco
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para os nossos modelos ORM
Base = declarative_base()

# Dependency do FastAPI para abrir e fechar a sessão por requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()