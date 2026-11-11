from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/pedidos", tags=["Pedidos"])

@router.post("/", response_model=schemas.PedidoResponse, status_code=201)
def criar_pedido(pedido: schemas.PedidoCreate, db: Session = Depends(get_db)):
    return crud.criar_pedido(db=db, pedido_in=pedido)

@router.get("/{pedido_id}", response_model=schemas.PedidoResponse)
def obter_pedido(pedido_id: int, db: Session = Depends(get_db)):
    return crud.obter_pedido(db=db, pedido_id=pedido_id)

@router.post("/{pedido_id}/cancelar", response_model=schemas.PedidoResponse)
def cancelar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    return crud.cancelar_pedido(db=db, pedido_id=pedido_id)