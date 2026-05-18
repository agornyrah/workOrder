from fastapi import FastAPI
from src.utils.db import Base, engine
from src.workorders.router import workOrder_router
from src.users.router import user_router, users_router
from src.activityLog.router import activityLog_router
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

#This is the permission method that allows sharing between your servers
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], #Allows only CORS with this server
    allow_credentials=True,
    allow_methods=["*"], #Allows ALL methods in the server
    allow_headers=["*"],
)

#Link the routes from the router.py file into the main backend server
app.include_router(workOrder_router)
app.include_router(user_router)
app.include_router(users_router)
app.include_router(activityLog_router)

Base.metadata.create_all(bind=engine)

