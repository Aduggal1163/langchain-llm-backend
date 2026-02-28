from fastapi import FastAPI,HTTPException,status,Depends
import models
from pydantic import BaseModel
from database import engine, sessionLocal
from typing import Annotated
from sqlalchemy.orm import Session
import uvicorn
app=FastAPI()
from fastapi.middleware.cors import CORSMiddleware
from seed_data import seed_database

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=engine)

def get_db():
    db=sessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session,Depends(get_db)]

#schemas

class UserCreate(BaseModel):
    username:str
    email:str

class ProductCreate(BaseModel):
    name:str
    price:float
    stock:int

class OrderCreate(BaseModel):
    total_amount:float

class OrderItemCreate(BaseModel):
    order_id:int
    product_id:int
    quantity:int

#API's

#USERS
@app.post("/users",status_code=status.HTTP_201_CREATED)
async def create_users(user: UserCreate, db:db_dependency):
    user_details=models.User(
        username = user.username,
        email = user.email
    )
    db.add(user_details)
    db.commit()
    db.refresh(user_details)
    return {
    "message": "User created successfully",
    "user": user_details
    }

@app.get('/users',status_code=status.HTTP_200_OK)
async def get_users(db:db_dependency):
    return db.query(models.User).all()

@app.get('/user/{user_id}',status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int,db:db_dependency):
    # all_users = db.query(models.User).all()
    # for user in all_users:
    #     if(user.id == user_id):
    #         return{
    #             'status':status.HTTP_200_OK,
    #             'message':'user found successfully',
    #             'user':user
    #         }
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="User not found"
        )
    return{
        'status':status.HTTP_200_OK,
        'message':"User found successfully",
        'user':user
    }

@app.delete("/users/{user_id}",status_code=status.HTTP_200_OK)
async def delete_user(user_id: int, db:db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    # 3. If found, delete and commit
    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}


#Products
@app.post('/products',status_code=status.HTTP_201_CREATED)
async def create_product(product : ProductCreate, db: db_dependency):
    product_details = models.Product(
        name = product.name,
        price = product.price,
        stock = product.stock
    )
    db.add(product_details)
    db.commit()
    db.refresh(product_details)
    return {
        'message':"Product created Successfully",
        'product':product
    }

@app.get('/products',status_code=status.HTTP_200_OK)
async def get_all(db:db_dependency):
    return db.query(models.Product).all()

@app.get('/products/{id}',status_code=status.HTTP_200_OK)
async def products_id(id: int, db:db_dependency):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No product found with this id"
        )
    return {
        'message':"Product found",
        'product':product
    }

@app.delete('/products/{id}',status_code=status.HTTP_200_OK)
async def delete_product(id: int, db:db_dependency):
    product = db.query(models.Product).filter(models.Product.id == id).first()
    if product is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No product found with this id"
        )
    db.delete(product)
    db.commit()
    return {
        'message':"Product deleted successfully",
    }

#Create Order
@app.post("/users/{user_id}/orders",status_code=status.HTTP_201_CREATED)
async def create_order(user_id: int, order: OrderCreate, db:db_dependency):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    new_order = models.Order(
        total_amount=order.total_amount,
        user_id=user_id
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    return {
        "message": "Order created successfully",
        "order": new_order
    }

#Orders
@app.get('/orders',status_code=status.HTTP_200_OK)
async def get_orders(db:db_dependency):
    return db.query(models.Order).all()

@app.get('/orders/{id}',status_code=status.HTTP_200_OK)
async def order_by_id(id: int, db:db_dependency):
    order=db.query(models.Order).filter(models.Order.id == id).first()
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )

    return {
        "message": "Order fetched successfully",
        "order": order
    }

#update order status
@app.put('/orders/{id}',status_code=status.HTTP_200_OK)
async def update_status(id : int, db:db_dependency):
    order=db.query(models.Order).filter(models.Order.id == id).first()
    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found"
        )
    order.status = 'completed'
    db.commit()
    db.refresh(order)
    return {
        "message": "Order completed successfully",
        "order": order
    }

#Seed Database
@app.post("/seed",status_code=status.HTTP_201_CREATED)
async def seed_db():
    result = seed_database()
    return result

if __name__ =='__main__':
    uvicorn.run(app,host='localhost',port=8000)