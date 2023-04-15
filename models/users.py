from pydantic import BaseModel


# Entidad user
class User(BaseModel):
    username: str
    fullname: str
    email: str
    disabled: str
    password: str
    
class User_db(BaseModel):
    id: int
    username: str
    fullname: str
    email: str
    disabled: str
    password: str
    
    
class Coment(BaseModel):
    content: str
    
class Coment_db(BaseModel):
    id: int
    content: str
    id_user: int
    date: str
    hour: str
    
    
class User_coment(BaseModel):
    content: str
    fecha: str
    hora: str