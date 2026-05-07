from fastapi import FastAPI, Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from pydantic import BaseModel
from typing import List

# App Configuration
app = FastAPI(
    title="Tanaka’s Car Dealership",
    description="API for managing cars, purchases, and customer authentication.",
    version="8.2.4"
)
# Authentication Setup (HTTP Basic Auth)
security = HTTPBasic()

# Default username + password
USERS = {
    "tanaka": "tanaka123"
}

def auth(credentials: HTTPBasicCredentials = Depends(security)):
    password = USERS.get(credentials.username)
    if password != credentials.password:
        raise HTTPException(status_code=401, detail="Invalid username or password")
    return credentials.username

# Car Models & Storage
class Car(BaseModel):
    id: int
    name: str
    price: float
    description: str | None = None

cars: List[Car] = []

# Purchase Models & Storage
class PurchaseItem(BaseModel):
    car_id: int
    quantity: int

class Purchase(BaseModel):
    id: int
    items: List[PurchaseItem]
    total_price: float = 0

purchases: List[Purchase] = []

# Authentication Endpoints
@app.get("/login-required", tags=["Authentication"])
def login_required(user: str = Depends(auth)):
    return {"logged_in_as": user}

# Car Endpoints
@app.get("/cars", tags=["Cars"])
def get_cars(user: str = Depends(auth)):
    return cars

@app.post("/cars", tags=["Cars"])
def add_car(car: Car, user: str = Depends(auth)):
    cars.append(car)
    return car

@app.get("/cars/{car_id}", tags=["Cars"])
def get_car(car_id: int, user: str = Depends(auth)):
    for c in cars:
        if c.id == car_id:
            return c
    raise HTTPException(status_code=404, detail="Car not found")

@app.put("/cars/{car_id}", tags=["Cars"])
def update_car(car_id: int, updated: Car, user: str = Depends(auth)):
    for i, c in enumerate(cars):
        if c.id == car_id:
            cars[i] = updated
            return updated
    raise HTTPException(status_code=404, detail="Car not found")

@app.delete("/cars/{car_id}", tags=["Cars"])
def delete_car(car_id: int, user: str = Depends(auth)):
    for c in cars:
        if c.id == car_id:
            cars.remove(c)
            return {"message": "Car removed from dealership"}
    raise HTTPException(status_code=404, detail="Car not found")

# Purchase Endpoints
@app.get("/purchases", tags=["Purchases"])
def get_purchases(user: str = Depends(auth)):
    return purchases

@app.post("/purchases", tags=["Purchases"])
def create_purchase(purchase: Purchase, user: str = Depends(auth)):
    total = 0
    for item in purchase.items:
        for c in cars:
            if c.id == item.car_id:
                total += c.price * item.quantity

    purchase.total_price = total
    purchases.append(purchase)
    return purchase

@app.get("/purchases/{purchase_id}", tags=["Purchases"])
def get_purchase(purchase_id: int, user: str = Depends(auth)):
    for p in purchases:
        if p.id == purchase_id:
            return p
    raise HTTPException(status_code=404, detail="Purchase not found")
