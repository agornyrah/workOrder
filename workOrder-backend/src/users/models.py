from sqlalchemy import Column, Integer, String
from src.utils.db import Base

class UserModel(Base):
    __tablename__ = "user_table"

    user_id = Column(Integer, primary_key=True, index=True)
    full_name = Column(String, index=True)
    email = Column(String)
    role = Column(String)
    hash_password = Column(String)
