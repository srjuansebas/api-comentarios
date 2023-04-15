from fastapi import FastAPI, Depends
from routers import crear_usuario, crear_comentario, login



app = FastAPI()




# Routers 
app.include_router(crear_usuario.router)
app.include_router(crear_comentario.router)
app.include_router(login.router)


    



@app.get("/")
async def root():
    return  {"saludo": "bienvenido a tu api de comentarios"}


contraseña_db = "sha41HYqXgSIl0T77sad"