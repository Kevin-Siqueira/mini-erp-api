from pydantic import BaseModel, EmailStr, Field
from typing import List
from decimal import Decimal
from datetime import datetime
from app.models import StatusPedido

# --- SCHEMAS DE CLIENTE ---
class ClienteBase(BaseModel):
    nome: str
    email: EmailStr
    cpf_cnpj: str

class ClienteCreate(ClienteBase):
    pass

class ClienteResponse(ClienteBase):
    id: int

    class Config:
        from_attributes = True


# --- SCHEMAS DE PRODUTO ---
class ProdutoBase(BaseModel):
    nome: str
    preco: Decimal = Field(gt=0, description="O preço deve ser maior que zero")
    estoque: int = Field(ge=0, description="O estoque não pode ser negativo")

class ProdutoCreate(ProdutoBase):
    pass

class ProdutoResponse(ProdutoBase):
    id: int

    class Config:
        from_attributes = True


# --- SCHEMAS DE ITEM DO PEDIDO ---
class ItemPedidoCreate(BaseModel):
    produto_id: int
    quantidade: int = Field(gt=0, description="A quantidade deve ser maior que zero")

class ItemPedidoResponse(BaseModel):
    id: int
    produto_id: int
    quantidade: int
    preco_unitario: Decimal

    class Config:
        from_attributes = True


# --- SCHEMAS DE PEDIDO ---
class PedidoCreate(BaseModel):
    cliente_id: int
    itens: List[ItemPedidoCreate]

class PedidoResponse(BaseModel):
    id: int
    cliente_id: int
    status: StatusPedido
    valor_total: Decimal
    data_criacao: datetime
    itens: List[ItemPedidoResponse]

    class Config:
        from_attributes = True