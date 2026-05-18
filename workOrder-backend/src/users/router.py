from fastapi import APIRouter, Depends
from src.users import controller
from src.users.dtos import UserSchema, LoginSchema, UserResponseSchema, UpdateUserSchema
from src.utils.db import get_db
from fastapi import status, Request
from sqlalchemy.orm import Session

#Create a route instance with a prefix user in the links or domains
user_router = APIRouter(prefix="/auth")

#Create a route instance for general user management
users_router = APIRouter(prefix="/users")

#Create a route to create a user
@user_router.post("/register", response_model=UserResponseSchema, status_code=status.HTTP_200_OK)
def user_register(user: UserSchema, db: Session = Depends(get_db)):
    return controller.register(user, db)


###########################################################################################

#Create a route to get all users
@users_router.get("", status_code=status.HTTP_200_OK)
def user_get_all_users(role: str | None = None, db: Session = Depends(get_db)):
    users = controller.get_all_users(db)
    if role:
        role_lower = role.lower()
        users = [user for user in users if user.role and user.role.lower() == role_lower]
    return [
        {
            "id": user.user_id,
            "email": user.email,
            "name": user.full_name,
            "role": user.role
        }
        for user in users
    ]


###########################################################################################

#Create a route to fetch a user by ID
@users_router.get("/{id}", status_code=status.HTTP_200_OK)
def user_get_by_id(id: int, db: Session = Depends(get_db)):
    user = controller.get_user_by_id(id, db)
    return {
        "id": user.user_id,
        "email": user.email,
        "name": user.full_name,
        "role": user.role
    }


###########################################################################################

#Create a route to login a user
@user_router.post("/login", status_code=status.HTTP_200_OK)
def user_login(user: LoginSchema, db: Session = Depends(get_db)):
    return controller.login(user, db)


###########################################################################################

#Create a route to authenticate tokens
@user_router.get("/me", status_code=status.HTTP_200_OK)
def user_authenticate(request: Request, db: Session = Depends(get_db)):
    user = controller.is_authenticated(request, db)
    return {
        "id": user.user_id,
        "email": user.email,
        "name": user.full_name,
        "role": user.role
    }


#Create a route to edit a user
@users_router.put("/{id}", status_code=status.HTTP_200_OK)
def user_update(id: int, user_updates: UpdateUserSchema, db: Session = Depends(get_db)):
    user = controller.update_user_by_id(id, user_updates, db)
    return {
        "id": user.user_id,
        "email": user.email,
        "name": user.full_name,
        "role": user.role
    }

#Create a route to delete a user
@users_router.delete("/{id}", status_code=status.HTTP_200_OK)
def user_delete(id: int, db: Session = Depends(get_db)):
    return controller.delete_user_by_id(id, db)
