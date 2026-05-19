from sqlalchemy import Column, Integer, String, ForeignKey
from src.utils.db import Base

class WorkOrder(Base):
    __tablename__ = "workOrders_table"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    priority = Column(String)
    site = Column(String)
    status = Column(String, default="open")
    createdAt = Column(String)
    dueDate = Column(String)
    equipment = Column(String)
    assignedTo = Column(String)
    createdBy = Column(String)
    createdById = Column(Integer, ForeignKey("user_table.user_id", ondelete="SET NULL"))

    #This is where you initialize linkage between some users and the work orders assigned to them specifically
    user_id = Column(Integer, ForeignKey("user_table.user_id", ondelete="CASCADE"))

