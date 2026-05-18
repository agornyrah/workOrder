from fastapi import HTTPException, Request
from src.users.dtos import UserSchema, LoginSchema, UpdateUserSchema
from sqlalchemy.orm import Session
from src.users.models import UserModel
from fastapi import status
from src.utils.settings import settings
import jwt
from jwt.exceptions import InvalidTokenError

#########################################################################################################################
#An import that allows you to add dates and time unto your code
from datetime import datetime, timedelta


#########################################################################################################################
#An IMPORT and an INSTANCE are created to enable password hashing unto the database from user inputs
from pwdlib import PasswordHash
password_hash = PasswordHash.recommended()

#A function that applies the hashing to the password
def get_password_hash(password: str):
    return password_hash.hash(password)

#A function that verifies password matches
def verify_password(plain_password, hashed_password):
    return password_hash.verify(plain_password, hashed_password)
#########################################################################################################################

def register(user: UserSchema, db: Session):

    #First, Check if the full_name already exists
    db_full_name_and_email = db.query(UserModel).filter(UserModel.full_name == user.full_name).first()
    if db_full_name_and_email:
        raise HTTPException(status_code=400, detail="Full name already exists")

    #Second, Check and validate email
    db_full_name_and_email = db.query(UserModel).filter(UserModel.email == user.email).first()
    if db_full_name_and_email:
        raise HTTPException(status_code=400, detail="Email already exists")
    
    #Third, Hash password
    db_hashed_password = get_password_hash(user.hash_password)

    #Fourth, Create a new user to be added to the database
    db_user = UserModel(
        full_name = user.full_name,
        email = user.email,
        role = user.role,
        hash_password = db_hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user
    #return {"User registered successfully"}


#########################################################################################################################

def get_all_users(db: Session):
    #Get all users from the database
    db_users = db.query(UserModel).all()
    
    return db_users

#########################################################################################################################

def login(user: LoginSchema, db: Session):

    #First, Check if the user email matches
    db_login_user_email_and_password = db.query(UserModel).filter(UserModel.email == user.email).first()
    if not db_login_user_email_and_password:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid email.")
    
    #Second, check if password matches
    if not verify_password(user.password, db_login_user_email_and_password.hash_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password.") 
    
    #A variable that calculates the current time the user logs in and adds the expiry time till the user logs out automatically
    exp_time = datetime.now() + timedelta(minutes=settings.EXPIRY_TIME)
    print(exp_time)  #Display and see time differences in the terminal

    #Third, generate a token that is valid after some time
    token = jwt.encode(
        {"user_id": db_login_user_email_and_password.user_id, "exp": int(exp_time.timestamp())},  #Payload data that is used to encode to make the jwt token
        settings.SECRET_KEY,
        settings.ALGORITHM
    )
    
    return {
        "access_token": token,
        "user": {
            "id": db_login_user_email_and_password.user_id,
            "email": db_login_user_email_and_password.email,
            "name": db_login_user_email_and_password.full_name,
            "role": db_login_user_email_and_password.role
        }
    }

#########################################################################################################################

def is_authenticated(request:Request, db: Session):
    #USE TRY and CATCH or EXCEPT to implement this ogic especially when the token is invalid or expired
    try:
        #Get the token that was generated once the user logged in and extract or 
        #find the value of the authorization key in the headers object
        token = request.headers.get("authorization")

        if not token:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token not found.")
        
        #NB normally, generated tokens have the prefix "jwt" prepended to it 7
        #so this step actually removes that and helps us validate the token alone
        token = token.split(" ")[-1]

        #Decode the token and verify it with the params that were used to create it
        data = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)

        #Get the user_id and the expiry time from the decoded token
        token_user_id = data.get("user_id")
        exp_time = data.get("exp")

        #Compare expiry time to a current time
        current_time = datetime.now().timestamp()
        if not exp_time or current_time > exp_time:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired.")
        
        #Check if the user_id matches the one in the database
        user = db.query(UserModel).filter(UserModel.user_id == token_user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid User ID.")
        
        return user
    
    except InvalidTokenError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are UNAUTHORIZED")

###########################################################################################

#Logic to carry out the EDIT/UPDATE User request

###########################################################################################
#Logic to carry out the DELETE USER request
def delete_user_by_id(id: int, db: Session):

    #First, query the database for the user with the specified ID
    db_delete_user_by_id = db.query(UserModel).filter(UserModel.user_id == id).first()

    #Second, get the user and apply the delete method to remove it from the database
    if db_delete_user_by_id is not None:
        db.delete(db_delete_user_by_id)
        db.commit()

        return {"User removed successfully"}
    
    return None 


###########################################################################################
#Logic to carry out the GET USER BY ID request
def get_user_by_id(id: int, db: Session):
    db_user = db.query(UserModel).filter(UserModel.user_id == id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID NOT FOUND")
    return db_user


###########################################################################################
#Logic to carry out the EDIT/UPDATE User request
def update_user_by_id(id: int, user_updates: UpdateUserSchema, db: Session):
    db_user = db.query(UserModel).filter(UserModel.user_id == id).first()
    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User ID NOT FOUND")
    
    # Check if new email is already taken by someone else
    if user_updates.email != db_user.email:
        existing_email = db.query(UserModel).filter(UserModel.email == user_updates.email).first()
        if existing_email:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already exists")
            
    setattr(db_user, "full_name", user_updates.name)
    setattr(db_user, "email", user_updates.email)
    setattr(db_user, "role", user_updates.role)
    
    db.commit()
    db.refresh(db_user)
    return db_user
