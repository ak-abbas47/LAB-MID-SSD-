from fastapi import FastAPI, Depends, HTTPException, Form
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from app.models import Base
import app.crud as crud

Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# -------------------------
# ROUTES — Accounts
# -------------------------

@app.get("/accounts/")
def get_accounts(db: Session = Depends(get_db)):
    return crud.get_all_accounts(db)

@app.post("/accounts/")
def create_account(
    holder_name: str = Form(...),
    email: str = Form(...),
    balance: float = Form(...),
    db: Session = Depends(get_db)
):
    return crud.add_account(db, holder_name, email, balance)

@app.put("/accounts/{id}")
def update_account(
    id: int,
    holder_name: str = Form(...),
    email: str = Form(...),
    balance: float = Form(...),
    db: Session = Depends(get_db)
):
    account = crud.update_account(db, id, holder_name, email, balance)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return account

@app.delete("/accounts/{id}")
def delete_account(id: int, db: Session = Depends(get_db)):
    account = crud.delete_account(db, id)
    if not account:
        raise HTTPException(status_code=404, detail="Account not found")
    return {"message": f"Account with ID {id} has been deleted"}

# -------------------------
# ROUTES — Transactions
# -------------------------

@app.get("/transactions/")
def get_transactions(db: Session = Depends(get_db)):
    return crud.get_all_transactions(db)

@app.post("/transactions/")
def create_transaction(
    account_id: int = Form(...),
    amount: float = Form(...),
    type: str = Form(...),
    db: Session = Depends(get_db)
):
    return crud.add_transaction(db, account_id, amount, type)

@app.put("/transactions/{id}")
def update_transaction(
    id: int,
    account_id: int = Form(...),
    amount: float = Form(...),
    type: str = Form(...),
    db: Session = Depends(get_db)
):
    transaction = crud.update_transaction(db, id, account_id, amount, type)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@app.delete("/transactions/{id}")
def delete_transaction(id: int, db: Session = Depends(get_db)):
    transaction = crud.delete_transaction(db, id)
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return {"message": f"Transaction with ID {id} has been deleted"}