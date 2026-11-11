from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from app import models, schemas

# --- CRUD CLIENTES ---
def criar_cliente(db: Session, cliente: schemas.ClienteCreate):
    # Verifica se já existe email ou CPF/CNPJ cadastrado
    db_cliente = db.query(models.Cliente).filter(
        (models.Cliente.email == cliente.email) | (models.Cliente.cpf_cnpj == cliente.cpf_cnpj)
    ).first()
    
    if db_cliente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cliente já cadastrado com este Email ou CPF/CNPJ."
        )

    novo_cliente = models.Cliente(**cliente.model_dump())
    db.add(novo_cliente)
    db.commit()
    db.refresh(novo_cliente)
    return novo_cliente

def listar_clientes(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Cliente).offset(skip).limit(limit).all()

def obter_cliente(db: Session, cliente_id: int):
    cliente = db.query(models.Cliente).filter(models.Cliente.id == cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado.")
    return cliente


# --- CRUD PRODUTOS ---
def criar_produto(db: Session, produto: schemas.ProdutoCreate):
    novo_produto = models.Produto(**produto.model_dump())
    db.add(novo_produto)
    db.commit()
    db.refresh(novo_produto)
    return novo_produto

def listar_produtos(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Produto).offset(skip).limit(limit).all()

def obter_produto(db: Session, produto_id: int):
    produto = db.query(models.Produto).filter(models.Produto.id == produto_id).first()
    if not produto:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Produto não encontrado.")
    return produto
# --- CRUD & REGRAS DE NEGÓCIO DE PEDIDOS ---

def criar_pedido(db: Session, pedido_in: schemas.PedidoCreate):
    # 1. Verificar se o cliente existe
    cliente = db.query(models.Cliente).filter(models.Cliente.id == pedido_in.cliente_id).first()
    if not cliente:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente não encontrado.")

    if not pedido_in.itens:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="O pedido deve conter pelo menos um item.")

    valor_total = 0
    itens_db = []

    # Processa cada item do pedido
    for item in pedido_in.itens:
        # Bloqueia a linha do produto no banco para evitar concorrencia (race conditions)
        produto = db.query(models.Produto).filter(models.Produto.id == item.produto_id).with_for_update().first()
        
        if not produto:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail=f"Produto ID {item.produto_id} não encontrado."
            )

        # Regra de negócio 1: Não vender acima do estoque
        if produto.estoque < item.quantidade:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Estoque insuficiente para o produto '{produto.nome}'. Disponível: {produto.estoque}, Solicitado: {item.quantidade}."
            )

        # Atualiza o estoque do produto
        produto.estoque -= item.quantidade

        # Regra de negócio 2: Subtotal e Total calculados a partir dos itens
        subtotal = produto.preco * item.quantidade
        valor_total += subtotal

        item_db = models.ItemPedido(
            produto_id=produto.id,
            quantidade=item.quantidade,
            preco_unitario=produto.preco
        )
        itens_db.append(item_db)

    novo_pedido = models.Pedido(
        cliente_id=pedido_in.cliente_id,
        valor_total=valor_total,
        status=models.StatusPedido.CONCLUIDO,
        itens=itens_db
    )

    db.add(novo_pedido)
    db.commit()
    db.refresh(novo_pedido)
    return novo_pedido


def obter_pedido(db: Session, pedido_id: int):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado.")
    return pedido


def cancelar_pedido(db: Session, pedido_id: int):
    pedido = db.query(models.Pedido).filter(models.Pedido.id == pedido_id).first()
    
    if not pedido:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Pedido não encontrado.")
    
    if pedido.status == models.StatusPedido.CANCELADO:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Este pedido já está cancelado.")

    # Regra de negócio 3: Cancelar pedido devolve o estoque
    for item in pedido.itens:
        produto = db.query(models.Produto).filter(models.Produto.id == item.produto_id).first()
        if produto:
            produto.estoque += item.quantidade

    pedido.status = models.StatusPedido.CANCELADO
    db.commit()
    db.refresh(pedido)
    return pedido