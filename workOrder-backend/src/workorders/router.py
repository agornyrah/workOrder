from fastapi import APIRouter, Depends
from src.workorders import controller
from src.workorders.dtos import WorkSchema, WorkResponseSchema, StatusUpdateSchema
from src.utils.db import get_db
from fastapi import status
from typing import List
from sqlalchemy.orm import Session
from src.utils.helpers import is_authenticated
from src.users.models import UserModel


#Create a route instance with a prefix workorders in the links or domains
workOrder_router = APIRouter(prefix="/workorders")

#Create a route to create a work order
@workOrder_router.post("",response_model=WorkResponseSchema, status_code=status.HTTP_201_CREATED)
def create_workOrder(workOrder: WorkSchema, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    
    #This is used to produce the id of the user who created the particular workOrder
    print(user.user_id) 

    return controller.create_workOrder(workOrder, db, user)

#NB:
#The response_model parameter is used to define the structure of the response data.
#And it only gives me the fields in the response i want to see / display

#NB:
#user:UserModel = Depends(is_authenticated) is for dependency injection 
#such that only authorized users can access apis

###########################################################################################

#Create a route to fetch all work orders
@workOrder_router.get("",response_model=List[WorkResponseSchema], status_code=status.HTTP_200_OK)
def fetch_workOrders(db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.get_workOrders(db, user) #Return a workorder based on a logged in user

#We use LIST here becaue there would be alot of objects in the response body

###########################################################################################

#Create a route to fetch a work order by ID
@workOrder_router.get("/{id}",response_model=WorkResponseSchema, status_code=status.HTTP_200_OK)
def fetch_workOrder_by_id(id: int, db: Session = Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.get_workOrder_by_id(db, id)

###########################################################################################

#Create a route to edit all work order
@workOrder_router.patch("/{id}",response_model=WorkResponseSchema, status_code=status.HTTP_200_OK)
def edit_workOrder_by_id(id: int, workOrder: WorkSchema, db: Session = Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.edit_workOrder_by_id(workOrder, db, id, user)

###########################################################################################

#Create a route to change status of a work order
@workOrder_router.patch("/{id}/status", response_model=WorkResponseSchema, status_code=status.HTTP_200_OK)
def update_workOrder_status(id: int, status_update: StatusUpdateSchema, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.update_workOrder_status(id, status_update, db, user)

###########################################################################################

#Create a route to delete a work order
@workOrder_router.delete("/{id}",response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete_workOrder_by_id(id: int, db: Session = Depends(get_db), user:UserModel = Depends(is_authenticated)):
    return controller.delete_workOrder_by_id(id, db, user)

###########################################################################################
