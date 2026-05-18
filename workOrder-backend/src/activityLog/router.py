from fastapi import APIRouter, Depends
from src.activityLog import controller
from src.activityLog.dtos import ActivitySchema, ActivityResponseSchema
from src.utils.db import get_db
from fastapi import status
from typing import List
from sqlalchemy.orm import Session
from src.utils.helpers import is_authenticated
from src.users.models import UserModel


#Create a route instance with a prefix activity-log in the links or domains
activityLog_router = APIRouter(prefix="/activity-log")

#Create a route to create an activity log entry
@activityLog_router.post("",response_model=ActivityResponseSchema, status_code=status.HTTP_201_CREATED)
def create_activity(activity: ActivitySchema, db: Session = Depends(get_db)):
    return controller.create_activity(activity, db)


###########################################################################################

#Create a route to fetch all activity logs
@activityLog_router.get("",response_model=List[ActivityResponseSchema], status_code=status.HTTP_200_OK)
def fetch_activities(db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.get_activities(db, user)


###########################################################################################

#Create a route to mark all activity logs as read for the current user
@activityLog_router.patch("/read-all", status_code=status.HTTP_200_OK)
def mark_all_read(db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.mark_all_activities_read(db, user)


###########################################################################################

#Create a route to mark a single activity log as read for the current user
@activityLog_router.patch("/{id}/read", status_code=status.HTTP_200_OK)
def mark_read(id: int, db: Session = Depends(get_db), user: UserModel = Depends(is_authenticated)):
    return controller.mark_activity_read(id, db, user)


###########################################################################################

#Create a route to fetch an activity log by ID
@activityLog_router.get("/{id}",response_model=ActivityResponseSchema, status_code=status.HTTP_200_OK)
def fetch_activity_by_id(id: int, db: Session = Depends(get_db)):
    return controller.get_activity_by_id(db, id)

###########################################################################################

#Create a route to delete an activity log
@activityLog_router.delete("/{id}",response_model=None, status_code=status.HTTP_204_NO_CONTENT)
def delete_activity_by_id(id: int, db: Session = Depends(get_db)):
    return controller.delete_activity_by_id(id, db)

###########################################################################################



