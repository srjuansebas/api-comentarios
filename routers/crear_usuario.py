from fastapi import APIRouter, HTTPException
from models.users import User, User_db
from jose import jwt
from routers.consultas import users_db, consultar, cursor, conexion


router = APIRouter()

ALGORITHM = "HS256"

SECRET = "12f7be59193e5661f5e0742590f32c314ddce75901406a40411b0833ef1b9c3e"







def codificar(valor):
    return jwt.encode(valor, SECRET , algorithm=ALGORITHM).get("valor")

def decodificar(valor):
    return jwt.decode(valor, SECRET, algorithms=[ALGORITHM]).get("valor")



def consultar():
    users_db.clear()
    cursor.execute("select * from usuario")
    consulta = cursor.fetchall()
    for usuario in consulta:
        users_db.append(User_db(id=usuario[0], username=usuario[1], fullname=usuario[2], email=usuario[3], disabled=usuario[4], password=usuario[5]))
        
    return users_db




def search_user(id: int):
    consultar()
    users = filter(lambda user: user.id == id, users_db)
    try:
        return list(users)[0]
    except:
       return {"error": "no se ha encontrado el usuario"}

def search_name(username: str):
    consultar()
    users = filter(lambda user: user.username == username, users_db)
    try:
        return list(users)[0]
    except:
       return {"error": "no se ha encontrado el usuario"}


@router.get("/get_user/{id}")
async def read_user(id: int):
    
    return search_user(id)

@router.get("/get_users")
async def users():
    consultar()
    return users_db

@router.post("/create_user", status_code=201)
async def create_user(user: User):
    
    consultar()
    while user.username in [user.username for user in users_db]:
        raise HTTPException(status_code=304, detail="el nombre de usuario ya existe, elige otro")
        
    if type(search_name(user.username)) == User:
        raise HTTPException(status_code=304, detail="no se ha podido crear el usuario")
    else:
        username: str = user.username
        fullname: str = user.fullname
        email: str = user.email
        disabled: str = user.disabled
        password: str = user.password
        cursor.execute(f"INSERT INTO usuario (nombre_usuario, nombre_completo, email, desabilitado, contraseña) VALUES ('{username}','{fullname}','{email}','{disabled}','{password}')")
        conexion.commit()
        return consultar()
    
    
@router.put("/create_user")
async def update_user(user: User_db): 
    consultar()
    found = False
    for index, saved_user in enumerate(users_db):
        if saved_user.id == user.id:
            users_db[index] = user
            id: int = user.id
            username: str = user.username
            fullname: str = user.fullname
            email: str = user.email
            disabled: str = user.disabled
            password: str = user.password
            cursor.execute(f"UPDATE usuario SET nombre_usuario='{username}', nombre_completo='{fullname}', email='{email}', desabilitado='{disabled}', contraseña='{password}' where id={id}")
            conexion.commit()
            found = True
            
    if not found:
        raise HTTPException(status_code=304, detail="no se ha actualizado el usuario")
    else:
        return consultar()



@router.delete("/create_user/{id}")
async def delete_user(id: int):
    found = False
    for index, saved_user in enumerate(users_db):
        if saved_user.id == id:
            del users_db[index]
            found = True
            cursor.execute(f"delete from usuario where id = {id}")
            conexion.commit()
    if not found:
        return {"error": "no se ha eliminado el usuario"}
    else:
        return consultar()
    

    
estructura = {
  "username": "elyisus",
  "fullname": "Jesus Lopez",
  "email": "jesuayisus@gmail.com",
  "disabled": "no",
  "password": "123456"
}

