from sqlalchemy import Column, Integer, String, Float
from .database import Base

class Account(Base):
    __tablename__ = "accounts"
    id = Column(Integer, primary_key=True, index=True)
    account_number = Column(String, unique=True, index=True)
    account_type = Column(String)  # e.g., 'savings', 'checking'
    balance = Column(Float)
    owner_name = Column(String)

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    account_id = Column(Integer)
    amount = Column(Float)
    type = Column(String) 