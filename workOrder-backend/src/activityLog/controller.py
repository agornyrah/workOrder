from fastapi import HTTPException
from src.activityLog.dtos import ActivitySchema
from sqlalchemy.orm import Session
from src.activityLog.models import ActivityLog, UserActivityHidden, UserActivityRead
from src.users.models import UserModel
from datetime import datetime

#NB: model_dump() converts a data from pydantic class to a dictionary

###########################################################################################
#Logic to carry out the CREATE ACTIVITY LOG request
def activity_response(activity: ActivityLog, read: bool = False):
    return {
        "log_id": activity.log_id,
        "id": activity.log_id,
        "action": activity.action,
        "workOrderId": activity.workOrderId,
        "workOrderTitle": activity.workOrderTitle,
        "performedBy": activity.performedBy,
        "note": activity.note or "",
        "timestamp": activity.timestamp or datetime.now().isoformat(),
        "read": read,
    }

###########################################################################################
#Logic to carry out the CREATE ACTIVITY LOG request
def create_activity(activityLogItem: ActivitySchema, db:Session, user: UserModel):

    #First receive and validate data
    new_activity = activityLogItem.model_dump()
    new_activity["performedBy"] = user.full_name
    new_activity["timestamp"] = datetime.now().isoformat()

    #Second, add data to databse by unpacking the data and using the database model as a blueprint
    db_new_activity = ActivityLog(**new_activity) 

    #Third, add the unpacked data to the database and save changes(commit)
    db.add(db_new_activity)
    db.commit()
    db.refresh(db_new_activity)
    
    #Improving endpoints for production:
    #This class is a performance format or practise to make the response more readable
    return activity_response(db_new_activity)

###########################################################################################
#Logic to carry out the GET ACTIVITY LOG request
def get_activities(db: Session, user: UserModel):

    #Fetch all read log IDs for this user
    read_log_ids = {r.log_id for r in db.query(UserActivityRead).filter(UserActivityRead.user_id == user.user_id).all()}
    hidden_log_ids = {h.log_id for h in db.query(UserActivityHidden).filter(UserActivityHidden.user_id == user.user_id).all()}

    #First, query(SEARCH/LOOP) the database for all visible activity logs and return ALL
    db_all_activities = (
        db.query(ActivityLog)
        .filter(ActivityLog.log_id.notin_(hidden_log_ids))
        .order_by(ActivityLog.log_id.desc())
        .all()
    )

    return [
        activity_response(activity, activity.log_id in read_log_ids)
        for activity in db_all_activities
    ]

###########################################################################################
#Logic to carry out the GET ACTIVITY LOG BY ID request
def get_activity_by_id(db: Session, id: int):

    #First, query the database for the work order with the specified ID
    db_getactivity_by_id = db.query(ActivityLog).filter(ActivityLog.log_id == id).first()
    
    if db_getactivity_by_id is None:
        return HTTPException(status_code=404, detail="Activity ID NOT FOUND", headers=None)
    
    return activity_response(db_getactivity_by_id)
    #return {"Activity fetched": db_getactivity_by_id}


###########################################################################################
#Logic to hide a single activity log entry for the current user
def delete_activity_by_id(id: int, db: Session, user: UserModel):

    #First, query the database for the work order with the specified ID
    db_deletactivity_by_id = db.query(ActivityLog).filter(ActivityLog.log_id == id).first()

    if db_deletactivity_by_id is None:
        raise HTTPException(status_code=404, detail="Activity ID NOT FOUND")

    existing_hidden = db.query(UserActivityHidden).filter(
        UserActivityHidden.user_id == user.user_id,
        UserActivityHidden.log_id == id
    ).first()

    if not existing_hidden:
        db.add(UserActivityHidden(user_id=user.user_id, log_id=id))
        db.commit()

    return {"message": "Activity hidden successfully"}


###########################################################################################
#Logic to hide all activity log entries for the current user
def delete_all_activities(db: Session, user: UserModel):
    activities = db.query(ActivityLog).all()
    hidden_log_ids = {h.log_id for h in db.query(UserActivityHidden).filter(UserActivityHidden.user_id == user.user_id).all()}

    for activity in activities:
        if activity.log_id not in hidden_log_ids:
            db.add(UserActivityHidden(user_id=user.user_id, log_id=activity.log_id))

    db.commit()

    return {"message": "All activity logs hidden for this user"}


###########################################################################################
#Logic to mark all activity log entries as read for the current user
def mark_all_activities_read(db: Session, user: UserModel):
    activities = db.query(ActivityLog).all()
    read_log_ids = {r.log_id for r in db.query(UserActivityRead).filter(UserActivityRead.user_id == user.user_id).all()}
    
    for activity in activities:
        if activity.log_id not in read_log_ids:
            new_read = UserActivityRead(user_id=user.user_id, log_id=activity.log_id)
            db.add(new_read)
    db.commit()
    return {"message": "All activities marked as read"}


###########################################################################################
#Logic to mark a single activity log entry as read for the current user
def mark_activity_read(id: int, db: Session, user: UserModel):
    activity = db.query(ActivityLog).filter(ActivityLog.log_id == id).first()
    if not activity:
        raise HTTPException(status_code=404, detail="Activity ID NOT FOUND")
        
    existing_read = db.query(UserActivityRead).filter(
        UserActivityRead.user_id == user.user_id,
        UserActivityRead.log_id == id
    ).first()
    
    if not existing_read:
        new_read = UserActivityRead(user_id=user.user_id, log_id=id)
        db.add(new_read)
        db.commit()
        
    return {"message": f"Activity {id} marked as read"}
