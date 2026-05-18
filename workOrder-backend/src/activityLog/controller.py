from fastapi import HTTPException
from src.activityLog.dtos import ActivitySchema
from sqlalchemy.orm import Session
from src.activityLog.models import ActivityLog, UserActivityRead
from src.users.models import UserModel

#NB: model_dump() converts a data from pydantic class to a dictionary

###########################################################################################
#Logic to carry out the CREATE ACTIVITY LOG request
def create_activity(activityLogItem: ActivitySchema, db:Session):

    #First receive and validate data
    new_activity = activityLogItem.model_dump()

    #Second, add data to databse by unpacking the data and using the database model as a blueprint
    db_new_activity = ActivityLog(**new_activity) 

    #Third, add the unpacked data to the database and save changes(commit)
    db.add(db_new_activity)
    db.commit()
    
    #Improving endpoints for production:
    #This class is a performance format or practise to make the response more readable
    return db_new_activity

###########################################################################################
#Logic to carry out the GET ACTIVITY LOG request
def get_activities(db: Session, user: UserModel):

    #First, query(SEARCH/LOOP) the database for all activity logs and return ALL
    db_all_activities = db.query(ActivityLog).all()

    #Fetch all read log IDs for this user
    read_log_ids = {r.log_id for r in db.query(UserActivityRead).filter(UserActivityRead.user_id == user.user_id).all()}

    #Dynamically set the read attribute for each activity log
    for activity in db_all_activities:
        activity.read = activity.log_id in read_log_ids

    return db_all_activities

###########################################################################################
#Logic to carry out the GET ACTIVITY LOG BY ID request
def get_activity_by_id(db: Session, id: int):

    #First, query the database for the work order with the specified ID
    db_getactivity_by_id = db.query(ActivityLog).filter(ActivityLog.log_id == id).first()
    
    if db_getactivity_by_id is None:
        return HTTPException(status_code=404, detail="Activity ID NOT FOUND", headers=None)
    
    return db_getactivity_by_id
    #return {"Activity fetched": db_getactivity_by_id}


###########################################################################################
#Logic to carry out the DELETE ACTIVITY LOG request
def delete_activity_by_id(id: int, db: Session):

    #First, query the database for the work order with the specified ID
    db_deletactivity_by_id = db.query(ActivityLog).filter(ActivityLog.log_id == id).first()

    #Second, get the workorder and apply the delete method to remove it from the database
    if db_deletactivity_by_id is not None:
        db.delete(db_deletactivity_by_id)
        db.commit()

        return {"Activity removed successfully"}
    
    return None 


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
