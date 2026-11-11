from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/clientes", tags=["Clientes"])

@router.post("/", response_model=schemas.ClienteResponse, status_code=201)
def criar_cliente(cliente: schemas.ClienteCreate, db: Session = Depends(get_db)):
    return crud.criar_cliente(db=db, cliente=cliente)

@router.get("/", response_model=List[schemas.ClienteResponse])
def listar_clientes(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.listar_clientes(db=db, skip=skip, limit=limit)

@router.get("/{cliente_id}", response_model=schemas.ClienteResponse)
def obter_cliente(cliente_id: int, db: Session = Depends(get_db)):
    return crud.obter_cliente(db=db, cliente_id=cliente_id)