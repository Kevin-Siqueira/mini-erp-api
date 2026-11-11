import enum
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, Enum, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base

# Enum para controlar o estado do pedido
class StatusPedido(str, enum.Enum):
    CONCLUIDO = "CONCLUIDO"
    CANCELADO = "CANCELADO"

class Cliente(Base):
    __tablename__ = "clientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    cpf_cnpj = Column(String(20), unique=True, nullable=False)

class Produto(Base):
    __tablename__ = "produtos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(100), nullable=False)
    preco = Column(Numeric(10, 2), nullable=False)
    estoque = Column(Integer, nullable=False, default=0)

class Pedido(Base):
    __tablename__ = "pedidos"

    id = Column(Integer, primary_key=True, index=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    data_criacao = Column(DateTime(timezone=True), server_default=func.now())
    status = Column(Enum(StatusPedido), default=StatusPedido.CONCLUIDO, nullable=False)
    valor_total = Column(Numeric(10, 2), nullable=False, default=0.0)

    # Relacionamentos
    cliente = relationship("Cliente")
    itens = relationship("ItemPedido", back_populates="pedido", cascade="all, delete-orphan")

class ItemPedido(Base):
    __tablename__ = "itens_pedido"

    id = Column(Integer, primary_key=True, index=True)
    pedido_id = Column(Integer, ForeignKey("pedidos.id"), nullable=False)
    produto_id = Column(Integer, ForeignKey("produtos.id"), nullable=False)
    quantidade = Column(Integer, nullable=False)
    preco_unitario = Column(Numeric(10, 2), nullable=False)

    # Relacionamentos
    pedido = relationship("Pedido", back_populates="itens")
    produto = relationship("Produto")