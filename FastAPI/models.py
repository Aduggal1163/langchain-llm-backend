from pydantic import BaseModel #for validation and In FastAPI we usually use Pydantic models for data.
class Product(BaseModel):
    id:int
    name:str
    description:str
    price:float
    quantity:int