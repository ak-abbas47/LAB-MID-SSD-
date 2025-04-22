from .models import Account, Transaction
from sqlalchemy.orm import Session
from datetime import datetime

# -----------------------
# Account CRUD
# -----------------------

def get_all_accounts(db: Session):
    return db.query(Account).all()

def get_account(db: Session, id: int):
    return db.query(Account).filter(Account.id == id).first()

def add_account(db: Session, holder_name: str, email: str, balance: float):
    account = Account(holder_name=holder_name, email=email, balance=balance)
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

def update_account(db: Session, id: int, holder_name: str, email: str, balance: float):
    account = get_account(db, id)
    if account:
        account.holder_name = holder_name
        account.email = email
        account.balance = balance
        db.commit()
    return account

def delete_account(db: Session, id: int):
    account = get_account(db, id)
    if account:
        db.delete(account)
        db.commit()
    return account

# -----------------------
# Transaction CRUD
# -----------------------

def get_all_transactions(db: Session):
    return db.query(Transaction).all()

def get_transaction(db: Session, id: int):
    return db.query(Transaction).filter(Transaction.id == id).first()

def add_transaction(db: Session, account_id: int, amount: float, type: str):
    transaction = Transaction(
        account_id=account_id,
        amount=amount,
        type=type,
        timestamp=datetime.utcnow()
    )
    db.add(transaction)

    # Update account balance if it's a valid deposit/withdraw
    account = get_account(db, account_id)
    if account:
        if type == "deposit":
            account.balance += amount
        elif type == "withdraw":
            if account.balance >= amount:
                account.balance -= amount
            else:
                return {"error": "Insufficient funds"}
        else:
            return {"error": "Invalid transaction type"}

    db.commit()
    db.refresh(transaction)
    return transaction

def update_transaction(db: Session, id: int, account_id: int, amount: float, type: str):
    transaction = get_transaction(db, id)
    if transaction:
        transaction.account_id = account_id
        transaction.amount = amount
        transaction.type = type
        transaction.timestamp = datetime.utcnow()
        db.commit()
    return transaction

def delete_transaction(db: Session, id: int):
    transaction = get_transaction(db, id)
    if transaction:
        db.delete(transaction)
        db.commit()
    return transaction