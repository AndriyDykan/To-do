from fastapi import FastAPI
from app.database.database import Base,engine
from app.routers import login,task,user


Base.metadata.create_all(bind=engine)

app = FastAPI()



app.include_router(user.router)
app.include_router(task.router)
app.include_router(login.router)