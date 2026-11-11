def test_regra_nao_vender_acima_do_estoque(client):
    # 1. Cadastra Cliente
    cliente_resp = client.post("/clientes/", json={"nome": "Ana", "email": "ana@test.com", "cpf_cnpj": "111"})
    cliente_id = cliente_resp.json()["id"]

    # 2. Cadastra Produto com estoque = 5
    prod_resp = client.post("/produtos/", json={"nome": "Teclado", "preco": 100.0, "estoque": 5})
    prod_id = prod_resp.json()["id"]

    # 3. Tenta comprar 10 unidades (deve falhar com status 400)
    pedido_data = {
        "cliente_id": cliente_id,
        "itens": [{"produto_id": prod_id, "quantidade": 10}]
    }
    response = client.post("/pedidos/", json=pedido_data)
    assert response.status_code == 400
    assert "Estoque insuficiente" in response.json()["detail"]


def test_criar_pedido_calcula_total_e_reduz_estoque(client):
    cliente_resp = client.post("/clientes/", json={"nome": "Bruno", "email": "bruno@test.com", "cpf_cnpj": "222"})
    cliente_id = cliente_resp.json()["id"]

    prod_resp = client.post("/produtos/", json={"nome": "Mouse", "preco": 50.0, "estoque": 10})
    prod_id = prod_resp.json()["id"]

    # Compra 2 unidades a 50.0 = Total 100.0
    pedido_data = {
        "cliente_id": cliente_id,
        "itens": [{"produto_id": prod_id, "quantidade": 2}]
    }
    response = client.post("/pedidos/", json=pedido_data)
    assert response.status_code == 201
    assert float(response.json()["valor_total"]) == 100.0

    # Verifica se o estoque reduziu para 8
    prod_consultado = client.get(f"/produtos/{prod_id}")
    assert prod_consultado.json()["estoque"] == 8


def test_cancelar_pedido_devolve_estoque(client):
    cliente_resp = client.post("/clientes/", json={"nome": "Carla", "email": "carla@test.com", "cpf_cnpj": "333"})
    cliente_id = cliente_resp.json()["id"]

    prod_resp = client.post("/produtos/", json={"nome": "Monitor", "preco": 500.0, "estoque": 5})
    prod_id = prod_resp.json()["id"]

    # Cria pedido de 2 unidades
    pedido_resp = client.post("/pedidos/", json={
        "cliente_id": cliente_id,
        "itens": [{"produto_id": prod_id, "quantidade": 2}]
    })
    pedido_id = pedido_resp.json()["id"]

    # Cancela o pedido
    cancel_resp = client.post(f"/pedidos/{pedido_id}/cancelar")
    assert cancel_resp.status_code == 200
    assert cancel_resp.json()["status"] == "CANCELADO"

    # Verifica se o estoque voltou para 5
    prod_consultado = client.get(f"/produtos/{prod_id}")
    assert prod_consultado.json()["estoque"] == 5