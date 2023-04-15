from fastapi import APIRouter, HTTPException, status, Depends
from models.users import Coment_db, Coment, User_coment
from routers.consultas import cursor, consultar_comentarios, conexion
from routers.login import oauth2, ALGORITHM, SECRET, search_user_db
from jose import jwt, JWTError


router = APIRouter()

users_coments = []


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



@router.get("/comentarios")
async def obtener_comentarios():
    cursor.execute(f"SELECT * FROM comentarios order by fecha, hora")
    comentarios = []
    try:
        for comentario in cursor.fetchall():
            comentarios.append(Coment_db(id=comentario[0], content=comentario[1], id_user=comentario[2], date=str(comentario[3]), hour=str(comentario[4])))
    except: 
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT, detail="no se ha actualizado el usuario")
    
    return comentarios 


@router.post("/comentar")
async def comentar(comentario: Coment, username: str = Depends(usuario_actual)):
    content: str = comentario.content
    user_id = search_user_db(username).id
    try:
        cursor.execute(f"INSERT INTO comentarios (comentario, id_usuario, fecha, hora) VALUES ('{content}', {user_id}, curdate(), date_format(now(), '%H:%i:%S'))")
        conexion.commit()
    except:
        raise HTTPException(status_code=304, detail="no se ha podido comentar")
    
    return consultar_comentarios()



# con esta funcion voy a traer los comentarios del usuario actual
@router.get("/user/coments")
async def usuario_comentarios(token: str = Depends(oauth2)):
    
    exeption = HTTPException(status_code=status.HTTP_204_NO_CONTENT,
                            detail="algo salio mal", 
                            headers={"WWW-Authenticate": "Bearer"})
    
    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        id_user = search_user_db(username).id
        cursor.execute(f"SELECT * FROM comentarios where id_usuario = {id_user}")
        for comentario in cursor.fetchall():
            users_coments.append(User_coment(content=comentario[1], fecha=str(comentario[3]), hora=str(comentario[4])))
    except:
        raise exeption
    
    
    
    
    return users_coments

