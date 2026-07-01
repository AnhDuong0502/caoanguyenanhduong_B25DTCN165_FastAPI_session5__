from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

products = [
    {"id": 1, "code": "SP001", "name": "Keyboard", "price": 500000, "stock": 10},
    {"id": 2, "code": "SP002", "name": "Mouse", "price": 300000, "stock": 5},
]


class Product(BaseModel):
    code: str
    name: str = Field(..., min_length=1)
    price: float = Field(..., gt=0)
    stock: int = Field(..., ge=0)


@app.put("/products/{product_id}")
def update_product(product_id: int, product: Product):
    current_product = None

    for p in products:
        if p["id"] == product_id:
            current_product = p
            break

    if current_product is None:
        raise HTTPException(status_code=404, detail="Product not found")

    for p in products:
        if p["code"] == product.code and p["id"] != product_id:
            raise HTTPException(status_code=400, detail="Product code already exists")

    current_product["code"] = product.code
    current_product["name"] = product.name
    current_product["price"] = product.price
    current_product["stock"] = product.stock

    return current_product
