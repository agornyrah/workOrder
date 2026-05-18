from fastapi import HTTPException
from src.workorders.dtos import WorkSchema, WorkResponseSchema, StatusUpdateSchema
from sqlalchemy.orm import Session
from src.workorders.models import WorkOrder
from src.users.models import UserModel

#NB: model_dump() converts a data from pydantic class to a dictionary

###########################################################################################
#Logic to carry out the CREATE WORKORDER request
def create_workOrder(workOrderItem: WorkSchema, db:Session, user: UserModel):

    #First receive and validate data
    new_workOrder = workOrderItem.model_dump()

    #Second, add data to databse by unpacking the data and using the database model as a blueprint
    db_new_workOrder = WorkOrder(
            id = new_workOrder["id"],
            title = new_workOrder["title"],
            description = new_workOrder["description"],
            priority = new_workOrder["priority"],
            site = new_workOrder["site"],
            status = new_workOrder["status"],
            created_at = new_workOrder["created_at"],
            due_date = new_workOrder["due_date"],

            #Adding the foreign key column to specify the workOrder creator owner
            user_id = user.user_id,
            ) 

    #Third, add the unpacked data to the database and save changes(commit)
    db.add(db_new_workOrder)
    db.commit()
    
    #Improving endpoints for production:
    #This class is a performance format or practise to make the response more readable
    return db_new_workOrder

###########################################################################################
#Logic to carry out the GET WORKORDER request (based on the userID)
def get_workOrders(db: Session, user: UserModel):
    # If user is admin or supervisor, fetch all work orders
    if user.role in ["admin", "supervisor"]:
        return db.query(WorkOrder).all()
        
    # If technician, fetch only their assigned work orders
    return db.query(WorkOrder).filter(WorkOrder.user_id == user.user_id).all()
    #return {"WorkOrders": db_all_workOrders}

###########################################################################################
#Logic to carry out the GET WORKORDER BY ID request
def get_workOrder_by_id(db: Session, id: int):

    #First, query the database for the work order with the specified ID
    db_getworkOrder_by_id = db.query(WorkOrder).filter(WorkOrder.id == id).first()
    
    if db_getworkOrder_by_id is None:
        raise HTTPException(status_code=404, detail="WorkOrder ID NOT FOUND")
    
    return db_getworkOrder_by_id
    #return {"Work fetched": db_getworkOrder_by_id}

###########################################################################################
#Logic to carry out the EDIT/UPDATE WORKORDER request
def edit_workOrder_by_id(workOrderItem: WorkSchema, db: Session, id: int, user: UserModel):

    #First, query the database for the work order with the specified ID
    db_editworkOrder_by_id = db.query(WorkOrder).filter(WorkOrder.id == id).first()

    if db_editworkOrder_by_id is None:
        raise HTTPException(status_code=404, detail="WorkOrder ID NOT FOUND")

    if db_editworkOrder_by_id.user_id != user.user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to edit this workorder")

    #Second, get that workorder and update it with new inputs using setattr to satisfy strict linter checks
    setattr(db_editworkOrder_by_id, "title", workOrderItem.title)
    setattr(db_editworkOrder_by_id, "description", workOrderItem.description)
    setattr(db_editworkOrder_by_id, "priority", workOrderItem.priority)
    setattr(db_editworkOrder_by_id, "site", workOrderItem.site)
    setattr(db_editworkOrder_by_id, "status", workOrderItem.status)
    setattr(db_editworkOrder_by_id, "created_at", workOrderItem.created_at)
    setattr(db_editworkOrder_by_id, "due_date", workOrderItem.due_date)
    
    #Third, save changes
    db.commit()

    return db_editworkOrder_by_id


###########################################################################################
#Logic to carry out the DELETE WORKORDER request
def delete_workOrder_by_id(id: int, db: Session, user: UserModel):

    #First, query the database for the work order with the specified ID
    db_deleteworkOrder_by_id = db.query(WorkOrder).filter(WorkOrder.id == id).first()

    if db_deleteworkOrder_by_id is None:
        raise HTTPException(status_code=404, detail="WorkOrder ID NOT FOUND")

    if db_deleteworkOrder_by_id.user_id != user.user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this workorder")

    #Second, get the workorder and apply the delete method to remove it from the database
    db.delete(db_deleteworkOrder_by_id)
    db.commit()

    return {"WorkOrder removed successfully"}


###########################################################################################
#Logic to carry out the STATUS UPDATE request
def update_workOrder_status(id: int, status_update: StatusUpdateSchema, db: Session, user: UserModel):
    db_workorder = db.query(WorkOrder).filter(WorkOrder.id == id).first()
    if db_workorder is None:
        raise HTTPException(status_code=404, detail="WorkOrder ID NOT FOUND")
        
    # Technicians can only update status of their own work orders, admins/supervisors can update any
    if user.role not in ["admin", "supervisor"] and db_workorder.user_id != user.user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to update status for this workorder")
        
    setattr(db_workorder, "status", status_update.status)
    db.commit()
    db.refresh(db_workorder)
    return db_workorder
