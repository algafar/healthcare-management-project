from fastapi import APIRouter,Depends,status
from app.database import get_db
from crud import Manager
from sqlalchemy.orm import Session
from schemas import PaymentResponse,PaymentCreate
from typing import List
from fastapi import HTTPException
from model import Invoice
from sqlalchemy import select

router = APIRouter(prefix="/payments", tags=["Payment"])
manager = Manager()

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def add_payment(new_payment:PaymentCreate,db:Session = Depends(get_db)):
    result = db.execute(select(Invoice).where(Invoice.invoice_id == new_payment.invoice_id))
    invoice = result.scalars().first()
    if not invoice:
        raise HTTPException(
            status_code=404, detail=" invoice not found"
        )
    if new_payment.amount != invoice.total_amount:
        raise HTTPException(
            status_code=404, detail=" payment amount must match"
        )        
    return manager.create_payment(new_payment, db)

@router.get("/", response_model=List[PaymentResponse], status_code=status.HTTP_200_OK)
def get_payments(db:Session = Depends(get_db)):
    payments = manager.view_patients(db)
    return payments or []

@router.get("/{payment_id}", response_model=PaymentResponse, status_code=status.HTTP_200_OK)
def get_payment_byid(payment_id ,db:Session = Depends(get_db)):
    payment = manager.get_payment_by_id(db,payment_id)
    if payment is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Payment with id {payment_id} not found")
    return payment 