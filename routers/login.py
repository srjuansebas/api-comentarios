from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta
from models.users import User, Coment
from routers.consultas import users_db, consultar, cursor, conexion, consultar_comentarios
    




ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 5

SECRET = "8bc25bce94c99244fe2e12aa8d84569e145c26b040111b92efb63e57a7b2d7b6"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl="Login")

# este es el contexto de encriptación
crypt = CryptContext(schemes=["bcrypt"])



def search_user(username: str):
    consultar()
    for usuario in users_db:
        if usuario.username == username:
            fullname: str = usuario.fullname
            email: str = usuario.email
            disabled: str = usuario.disabled
            password: str = usuario.password
            return User(username=username, fullname=fullname, email=email, disabled=disabled, password=password)



def search_user_db(username: str):
    consultar()
    for usuario in users_db:
        if usuario.username == username:
            return usuario



@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    
    user_db = search_user_db(form.username)
    
    if not user_db.username:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="el usuario no es correcto")
    
    user = search_user_db(form.username)    
    
    # aqui estoy verificando que la contraseña que recibo sea igual a la contraseña encriptada que tiene el usuario en la base de datos
    # (la funcion "verify" comprueba la contraseña recibida como si esta estuviera encriptada)
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="la contraseña no es correcta")
    
    access_token = {"sub": user.username, 
                    "exp": datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION),
                    "id_user": user.id}
    
    return {"acces_token": jwt.encode(access_token, SECRET , algorithm=ALGORITHM) , "token_type": "bearer"}




async def auth_user(token: str = Depends(oauth2)):
    
    exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Credenciales de autenticacion invalidas", 
                            headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exeption             
    except JWTError:
        raise exeption
            
    return search_user(username)
        
    
    
    
async def current_user(user: User = Depends(auth_user)):
    
    deshabilitado = True if user.disabled == "si" else False
    if deshabilitado:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="Usuario inactivo")
    
    return user  


async def usuario_actual(token: str = Depends(oauth2)):
    exeption = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Credenciales de autenticacion invalidas", 
                            headers={"WWW-Authenticate": "Bearer"})
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exeption             
    except JWTError:
        raise exeption
        
    return username
    




@router.get("/user/me")
async def me(user: User = Depends(current_user)):
    return user



# @router.post("/comentar")
# async def comentar(comentario: Coment, username: str = Depends(usuario_actual)):
#     content: str = comentario.content
#     user_id = search_user_db(username).id
#     try:
#         cursor.execute(f"INSERT INTO comentarios (comentario, id_usuario, fecha, hora) VALUES ('{content}', {user_id}, curdate(), date_format(now(), '%H:%i:%S'))")
#         conexion.commit()
#     except:
#         raise HTTPException(status_code=304, detail="no se ha podido comentar")
    
#     return consultar_comentarios()


