from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Cloud E‑Commerce API")

# Authentication (HTTP Basic)
security = HTTPBasic()

# Default username + password
USERS = {
    "tanaka": "tanaka123"
}

def auth(credentials: HTTPBasicCredentials = Depends(security)):
    password = USERS.get(credentials.username)
    if password != credentials.password:
        raise HTTPException(status_code=401, detail="Bad login or password")
    return credentials.username

# Product Models & Storage
class Product(BaseModel):
    id: int
    name: str
    price: float
    description: str | None = None

products: List[Product] = []

# Order Models & Storage
class OrderItem(BaseModel):
    product_id: int
    quantity: int

class Order(BaseModel):
    id: int
    items: List[OrderItem]
    total_price: float

orders: List[Order] = []

# Product Endpoints
@app.get("/products")
def get_products(user: str = Depends(auth)):
    return products


@app.post("/products")
def create_product(product: Product, user: str = Depends(auth)):
    products.append(product)
    return product


@app.get("/products/{product_id}")
def get_product(product_id: int, user: str = Depends(auth)):
    for p in products:
        if p.id == product_id:
            return p
    raise HTTPException(status_code=404, detail="Product not found")


@app.put("/products/{product_id}")
def update_product(product_id: int, updated: Product, user: str = Depends(auth)):
    for i, p in enumerate(products):
        if p.id == product_id:
            products[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Product not found")


@app.delete("/products/{product_id}")
def delete_product(product_id: int, user: str = Depends(auth)):
    for p in products:
        if p.id == product_id:
            products.remove(p)
            return {"message": "Product deleted"}
    raise HTTPException(status_code=404, detail="Product not found")

# Order Endpoints
@app.get("/orders")
def get_orders(user: str = Depends(auth)):
    return orders


@app.post("/orders")
def create_order(order: Order, user: str = Depends(auth)):
    total = 0
    for item in order.items:
        for p in products:
            if p.id == item.product_id:
                total += p.price * item.quantity

    order.total_price = total
    orders.append(order)
    return order


@app.get("/orders/{order_id}")
def get_order(order_id: int, user: str = Depends(auth)):
    for o in orders:
        if o.id == order_id:
            return o
    raise HTTPException(status_code=404, detail="Order not found")

@app.get("/login-required")
def login_required(user: str = Depends(auth)):
    return {"logged_in_as": user}
