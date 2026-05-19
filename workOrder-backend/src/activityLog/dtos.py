from pydantic import BaseModel

class ActivitySchema(BaseModel):
    action: str
    workOrderId: int
    workOrderTitle: str
    performedBy: str | None = ""
    note: str | None = ""


#Improving endpoints for production:
#This class is a pperformance format or practise to make the response more readable
#This schema shows that in the response body, the ID shouldnt show
class ActivityResponseSchema(BaseModel):
    log_id: int
    id: int
    action: str
    workOrderId: int
    workOrderTitle: str
    performedBy: str
    note: str
    timestamp: str
    read: bool = False
