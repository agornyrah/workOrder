from pydantic import BaseModel

class WorkSchema(BaseModel):
    id: int
    title: str
    description: str
    priority: str
    site: str
    status: str
    created_at: str
    due_date: str

#Improving endpoints for production:
#This class is a performance format or practise to make the response more readable
#This schema shows that in the response body, the ID shouldnt show
class WorkResponseSchema(BaseModel):
    title: str
    description: str
    priority: str
    site: str
    status: str
    created_at: str
    due_date: str

    #Display or show the id value of the user each workorder is assigned
    user_id: int | None = 0


class StatusUpdateSchema(BaseModel):
    status: str
    notes: str | None = ""
    
