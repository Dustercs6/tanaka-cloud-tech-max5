@app.get("/products")
def get_products(credentials: HTTPBasicCredentials = Depends(security)):
    password = USERS.get(credentials.username)

    if password != credentials.password:
        raise HTTPException(status_code=401, detail="Bad login or password")

    return products
