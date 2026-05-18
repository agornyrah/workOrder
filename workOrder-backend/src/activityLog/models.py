from sqlalchemy import Column, Integer, String
from src.utils.db import Base

class ActivityLog(Base):
    __tablename__ = "activity_log"

    log_id = Column(Integer, primary_key=True, index=True)
    action = Column(String, index=True)
    workOrderId = Column(String)
    workOrderTitle = Column(String)
    performedBy = Column(String)
    note = Column(String)


class UserActivityRead(Base):
    __tablename__ = "user_activity_read"

    user_id = Column(Integer, primary_key=True, index=True)
    log_id = Column(Integer, primary_key=True, index=True)
