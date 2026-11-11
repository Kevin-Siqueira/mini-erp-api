# 📦 Mini-ERP API

API REST para gestão simplificada de vendas, produtos e stock desenvolvida em Python.

## 🚀 Tecnologias Utilizadas

- **Python 3.10+**
- **FastAPI** (framework web e documentação OpenAPI)
- **PostgreSQL** (base de dados relacional via Docker)
- **SQLAlchemy** (ORM)
- **Pydantic** (validação de schemas)
- **Pytest** (testes automatizados)

## ⚙️ Regras de Negócio Implementadas

- ❌ **Controlo de Stock:** Impede vendas acima da quantidade disponível em stock.
- 💰 **Cálculo Automático:** Calcula o valor total do pedido a partir dos itens solicitados.
- 🔄 **Devolução de Stock:** O cancelamento de um pedido devolve automaticamente as quantidades ao stock.

## 🛠️ Como Executar o Projeto

1. Clone o repositório:
```bash
git clone [https://github.com/seu-usuario/mini-erp-api.git](https://github.com/seu-usuario/mini-erp-api.git)
cd mini-erp-api```

Crie e ative o ambiente virtual:
```bash
python -m venv venv
# Windows:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate```

Instale as dependências:
```bash
pip install -r requirements.txt```

Suba a base de dados PostgreSQL via Docker:
```bash
docker-compose up -d```

Inicie a aplicação:
```bash
python -m uvicorn app.main:app --reload```

Aceda à documentação interativa em: http://127.0.0.1:8000/docs

🧪 Como Executar os Testes

```bash
pytest```

