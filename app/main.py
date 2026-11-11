from fastapi import FastAPI
from app.database import engine, Base
import app.models as models
from app.routers import clientes, produtos, pedidos

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mini-ERP API")

# Registra os routers
app.include_router(clientes.router)
app.include_router(produtos.router)
app.include_router(pedidos.router)

@app.get("/")
def root():
    return {"mensagem": "API do Mini-ERP está rodando com sucesso!"}