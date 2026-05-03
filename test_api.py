from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_create_product():
    product = {"id": 1, "name": "Phone", "price": 1000}
    r = client.post("/products", json=product)
    assert r.status_code == 200

def test_create_order_total():
    # product already created in previous test
    order = {
        "id": 1,
        "items": [{"product_id": 1, "quantity": 2}],
        "total_price": 0
    }
    r = client.post("/orders", json=order)
    assert r.status_code == 200
    assert r.json()["total_price"] == 2000
