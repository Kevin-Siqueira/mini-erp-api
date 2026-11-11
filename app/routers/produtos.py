from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app import schemas, crud
from app.database import get_db

router = APIRouter(prefix="/produtos", tags=["Produtos"])

@router.post("/", response_model=schemas.ProdutoResponse, status_code=201)
def criar_produto(produto: schemas.ProdutoCreate, db: Session = Depends(get_db)):
    return crud.criar_produto(db=db, produto=produto)

@router.get("/", response_model=List[schemas.ProdutoResponse])
def listar_produtos(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.listar_produtos(db=db, skip=skip, limit=limit)

@router.get("/{produto_id}", response_model=schemas.ProdutoResponse)
def obter_produto(produto_id: int, db: Session = Depends(get_db)):
    return crud.obter_produto(db=db, produto_id=produto_id)