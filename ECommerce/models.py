from sqlalchemy import ForeignKey,Column,Integer,String,Float,Enum
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__='users'
    id=Column(Integer,primary_key=True,index=True)
    username=Column(String(50),unique=True,nullable=False)
    email=Column(String(100),unique=True,nullable=False)

    orders = relationship('Order',back_populates='user')

class Product(Base):
    __tablename__='products'
    id=Column(Integer,primary_key=True,index=True)
    name=Column(String(50),nullable=False)
    price=Column(Float, nullable=False)
    stock=Column(Integer, default=0)

    order_items=relationship('OrderItem',back_populates='product')

class Order(Base):
    __tablename__='orders'
    id=Column(Integer,primary_key=True,index=True)
    total_amount=Column(Float,default=0.0)
    status = Column(
        Enum("pending", "completed", name="order_status"),
        default="pending"
    )
    user_id=Column(Integer,ForeignKey('users.id'),nullable=False)
    
    user=relationship('User',back_populates='orders')
    order_items=relationship('OrderItem',back_populates='order')

class OrderItem(Base):
    __tablename__='order_items'
    id=Column(Integer,primary_key=True,index=True)
    order_id=Column(Integer,ForeignKey('orders.id'))
    product_id=Column(Integer,ForeignKey('products.id'))
    quantity=Column(Integer,nullable=False)

    order=relationship('Order',back_populates='order_items')
    product=relationship('Product',back_populates='order_items')