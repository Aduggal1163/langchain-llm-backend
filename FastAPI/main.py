from fastapi import FastAPI,HTTPException, status
from models import Product
app=FastAPI()
# if u want to see responses beautifully then type localhost:portnumber/docs (swagger UI) swagger is just like postman 

products = [
    Product(id=1, name="Laptop", description="Gaming laptop", price=90000, quantity=5),
    Product(id=2, name="Phone", description="iPhone", price=70000, quantity=10),
    Product(id=3, name="Headphones", description="Noise cancelling headphones", price=8000, quantity=25),
    Product(id=4, name="Keyboard", description="Mechanical keyboard", price=3500, quantity=15),
    Product(id=5, name="Mouse", description="Wireless mouse", price=1200, quantity=30),
    Product(id=6, name="Monitor", description="27 inch 4K monitor", price=25000, quantity=8),
    Product(id=7, name="Tablet", description="Android tablet", price=18000, quantity=12),
    Product(id=8, name="Smartwatch", description="Fitness smartwatch", price=6000, quantity=20),
    Product(id=9, name="Speaker", description="Bluetooth speaker", price=3000, quantity=18),
    Product(id=10, name="Camera", description="DSLR camera", price=55000, quantity=6)
]

@app.on_event("startup")
def startup_message():
    print("Server is running on port 8000")

@app.get("/",status_code=status.HTTP_200_OK)
def greet():
    return {"message":"Welcome to my first web server in python"}

@app.get("/products",status_code=status.HTTP_200_OK)
def get_all_products():
    return products

@app.get("/product/{id}", status_code=status.HTTP_200_OK)
def get_product_by_id(id:int):
    for product in products:
        if(product.id == id):
            return product
        
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found"
    )

@app.post("/addproduct", status_code=status.HTTP_201_CREATED)
def add_product(product: Product):
    products.append(product)
    return product

@app.put("/update/{id}", status_code=status.HTTP_200_OK)
def update_product(id: int, product : Product):
    for i in range (len(products)):
        if(products[i].id==id):
            products[i]=product
            return {"message":"Product updated successfully","product":product}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found"
    )

@app.delete("/delete/{id}", status_code=status.HTTP_200_OK)
def del_product(id:int):
    for i in range(len(products)):
        if products[i].id == id:
            products.remove(products[i])
            return {"message": "product deleted"}
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Product not found"
    )