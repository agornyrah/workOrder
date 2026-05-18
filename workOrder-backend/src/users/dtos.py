from pydantic import BaseModel

class UserSchema(BaseModel):
    user_id: int
    full_name: str
    email: str
    role: str
    hash_password: str

class LoginSchema(BaseModel):
    email: str
    password: str



#Improving endpoints for production:
#This class is a pperformance format or practise to make the response more readable
#This schema shows that in the response body, the ID shouldnt show
class UserResponseSchema(BaseModel):
    user_id: int
    full_name: str
    email: str
    role: str


class UpdateUserSchema(BaseModel):
    name: str
    email: str
    role: str
