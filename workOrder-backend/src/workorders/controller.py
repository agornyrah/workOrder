from fastapi import HTTPException
from src.workorders.dtos import WorkSchema, WorkResponseSchema, StatusUpdateSchema
from sqlalchemy.orm import Session
from src.workorders.models import WorkOrder
from src.users.models import UserModel
from src.activityLog.models import ActivityLog
from datetime import datetime

#NB: model_dump() converts a data from pydantic class to a dictionary

def _work_order_response(db: Session, work_order: WorkOrder):
    creator_name = work_order.createdBy
    creator_id = work_order.createdById

    if not creator_name and creator_id:
        creator = db.query(UserModel).filter(UserModel.user_id == creator_id).first()
        creator_name = creator.full_name if creator else None

    if not creator_name:
        created_activity = (
            db.query(ActivityLog)
            .filter(
                ActivityLog.workOrderId == str(work_order.id),
                ActivityLog.action == "created",
            )
            .order_by(ActivityLog.log_id.asc())
            .first()
        )
        if created_activity:
            creator_name = created_activity.performedBy
            creator = db.query(UserModel).filter(UserModel.full_name == creator_name).first()
            creator_id = creator.user_id if creator else None

    return {
        "id": work_order.id,
        "title": work_order.title,
        "description": work_order.description,
        "priority": work_order.priority,
        "site": work_order.site,
        "status": work_order.status,
        "createdAt": work_order.createdAt,
        "dueDate": work_order.dueDate,
        "equipment": work_order.equipment,
        "assignedTo": work_order.assignedTo,
        "createdBy": creator_name or "",
        "createdById": creator_id,
        "user_id": work_order.user_id,
    }

###########################################################################################
#Logic to carry out the CREATE WORKORDER request
def create_workOrder(workOrderItem: WorkSchema, db:Session, user: UserModel):

    # Resolve assigned user ID from full name
    assigned_tech = db.query(UserModel).filter(UserModel.full_name == workOrderItem.assignedTo).first()
    assigned_tech_id = assigned_tech.user_id if assigned_tech else None

    # Generate creation date if not provided
    created_date = workOrderItem.createdAt or datetime.now().strftime("%Y-%m-%d")

    #Second, add data to databse using the database model as a blueprint
    db_new_workOrder = WorkOrder(
            title = workOrderItem.title,
            description = workOrderItem.description,
            priority = workOrderItem.priority,
            site = workOrderItem.site,
            status = workOrderItem.status or "open",
            createdAt = created_date,
            dueDate = workOrderItem.dueDate,
            equipment = workOrderItem.equipment,
            assignedTo = workOrderItem.assignedTo,
            createdBy = user.full_name,
            createdById = user.user_id,
            user_id = assigned_tech_id,
            ) 

    #Third, add the unpacked data to the database and save changes(commit)
    db.add(db_new_workOrder)
    db.commit()
    db.refresh(db_new_workOrder)
    
    #Improving endpoints for production:
    #This class is a performance format or practise to make the response more readable
    return _work_order_response(db, db_new_workOrder)

###########################################################################################
#Logic to carry out the GET WORKORDER request (based on the userID)
def get_workOrders(db: Session, user: UserModel):
    # If user is admin or supervisor, fetch all work orders
    if user.role in ["admin", "supervisor"]:
        work_orders = db.query(WorkOrder).all()
        return [_work_order_response(db, work_order) for work_order in work_orders]
        
    # If technician, fetch only their assigned work orders
    work_orders = db.query(WorkOrder).filter(WorkOrder.user_id == user.user_id).all()
    return [_work_order_response(db, work_order) for work_order in work_orders]
    #return {"WorkOrders": db_all_workOrders}

###########################################################################################
#Logic to carry out the GET WORKORDER BY ID request
def get_workOrder_by_id(db: Session, id: int):

    #First, query the database for the work order with the specified ID
    db_getworkOrder_by_id = db.query(WorkOrder).filter(WorkOrder.id == id).first()
    
    if db_getworkOrder_by_id is None:
        raise HTTPException(status_code=404, detail="WorkOrder ID NOT FOUND")
    
    return _work_order_response(db, db_getworkOrder_by_id)
    #return {"Work fetched": db_getworkOrder_by_id}

###########################################################################################
#Logic to carry out the EDIT/UPDATE WORKORDER request
def edit_workOrder_by_id(workOrderItem: WorkSchema, db: Session, id: int, user: UserModel):

    #First, query the database for the work order with the specified ID
    db_editworkOrder_by_id = db.query(WorkOrder).filter(WorkOrder.id == id).first()

    if db_editworkOrder_by_id is None:
        raise HTTPException(status_code=404, detail="WorkOrder ID NOT FOUND")

    if user.role not in ["admin", "supervisor"] and db_editworkOrder_by_id.user_id != user.user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to edit this workorder")

    # Resolve assigned user ID from full name
    assigned_tech = db.query(UserModel).filter(UserModel.full_name == workOrderItem.assignedTo).first()
    assigned_tech_id = assigned_tech.user_id if assigned_tech else None

    #Second, get that workorder and update it with new inputs using setattr to satisfy strict linter checks
    setattr(db_editworkOrder_by_id, "title", workOrderItem.title)
    setattr(db_editworkOrder_by_id, "description", workOrderItem.description)
    setattr(db_editworkOrder_by_id, "priority", workOrderItem.priority)
    setattr(db_editworkOrder_by_id, "site", workOrderItem.site)
    setattr(db_editworkOrder_by_id, "status", workOrderItem.status)
    setattr(db_editworkOrder_by_id, "dueDate", workOrderItem.dueDate)
    setattr(db_editworkOrder_by_id, "equipment", workOrderItem.equipment)
    setattr(db_editworkOrder_by_id, "assignedTo", workOrderItem.assignedTo)
    setattr(db_editworkOrder_by_id, "user_id", assigned_tech_id)
    
    #Third, save changes
    db.commit()
    db.refresh(db_editworkOrder_by_id)

    return _work_order_response(db, db_editworkOrder_by_id)


###########################################################################################
#Logic to carry out the DELETE WORKORDER request
def delete_workOrder_by_id(id: int, db: Session, user: UserModel):

    #First, query the database for the work order with the specified ID
    db_deleteworkOrder_by_id = db.query(WorkOrder).filter(WorkOrder.id == id).first()

    if db_deleteworkOrder_by_id is None:
        raise HTTPException(status_code=404, detail="WorkOrder ID NOT FOUND")

    if user.role not in ["admin", "supervisor"] and db_deleteworkOrder_by_id.user_id != user.user_id:
        raise HTTPException(status_code=403, detail="You are not authorized to delete this workorder")

    #Second, get the workorder and apply the delete method to remove it from the database
    db.delete(db_deleteworkOrder_by_id)
    db.commit()

    return {"message": "WorkOrder removed successfully"}


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
    return _work_order_response(db, db_workorder)
