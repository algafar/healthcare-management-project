from fastapi import APIRouter,Depends,status
from app.database import get_db
from crud import Manager
from sqlalchemy.orm import Session
from schemas import InvoiceCreate,InvoiceResponse
from typing import List
from fastapi import HTTPException

router = APIRouter(prefix="/invoices", tags=["Invoice"])
manager = Manager()

@router.post("/", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def add_invoice(new_invoice:InvoiceCreate,db:Session = Depends(get_db)):
    return manager.create_invoices(new_invoice, db)

@router.get("/", response_model=List[InvoiceResponse], status_code=status.HTTP_200_OK)
def get_invoices(db:Session = Depends(get_db)):
    invoices = manager.view_invoice(db)
    return invoices or []

@router.get("/{invoice_id}", response_model=InvoiceResponse, status_code=status.HTTP_200_OK)
def get_invoice_byid(invoice_id ,db:Session = Depends(get_db)):
    invoice = manager.get_invoice_by_id(db,invoice_id)
    if invoice is None:
        raise HTTPException(status_code= status.HTTP_404_NOT_FOUND, detail=f"Invoice with id {invoice_id} not found")
    return invoice 