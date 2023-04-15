import mysql.connector    
from models.users import User_db, Coment_db

conexion = mysql.connector.connect(
  host="b3u3jzmxbwxh5ejokmt1-mysql.services.clever-cloud.com",
  user="umlwvhny0xzxquig",
  password="sha41HYqXgSIl0T77sad",
  database="b3u3jzmxbwxh5ejokmt1",
  port="3306"
)

cursor = conexion.cursor()
users_db = []
coments = []

def consultar():
    users_db.clear()
    cursor.execute("select * from usuario")
    consulta = cursor.fetchall()
    for usuario in consulta:
        users_db.append(User_db(id=usuario[0], username=usuario[1], fullname=usuario[2], email=usuario[3], disabled=usuario[4], password=usuario[5]))
        
    return users_db    


def consultar_comentarios():
    coments.clear()
    cursor.execute("select * from comentarios")
    consulta = cursor.fetchall()
    for comentario in consulta:
        fecha = comentario[3]
        hora = comentario[4]
        coments.append(Coment_db(id=comentario[0], content=comentario[1], id_user=comentario[2], date=str(fecha), hour=str(hora)))
        
    return coments
