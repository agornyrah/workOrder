from pydantic import BaseModel

class WorkSchema(BaseModel):
    id: int | None = None
    title: str
    description: str
    priority: str
    site: str
    status: str | None = "open"
    createdAt: str | None = None
    dueDate: str
    equipment: str | None = ""
    assignedTo: str | None = "Unassigned"

#Improving endpoints for production:
#This class is a performance format or practise to make the response more readable
#This schema includes all fields required by the frontend, including id.
class WorkResponseSchema(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    site: str
    status: str
    createdAt: str
    dueDate: str
    equipment: str | None = ""
    assignedTo: str | None = "Unassigned"

    #Display or show the id value of the user each workorder is assigned
    user_id: int | None = 0


class StatusUpdateSchema(BaseModel):
    status: str
    notes: str | None = ""
    
