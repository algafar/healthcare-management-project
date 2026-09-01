from fastapi import APIRouter,Depends,status
from app.database import get_db
from crud import Manager
from sqlalchemy.orm import Session
from schemas import InvoiceCreate,InvoiceResponse
from typing import List
from fastapi import HTTPException
from model import Invoice
router = APIRouter(prefix="/invoices", tags=["Invoice"])
manager = Manager()

@router.post("/", response_model=InvoiceResponse, status_code=status.HTTP_201_CREATED)
def add_invoice(new_invoice:InvoiceCreate,db:Session = Depends(get_db)):
    appointment = manager.appointment(db,new_invoice.appointment_id)
    existing_invoice = manager.get_invoice_by_appointment(db,new_invoice.appointment_id)
    if existing_invoice:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="An invoice  has already been generted or th this appointment"
        )
    if not appointment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Appointment not found"
        )
    if appointment.status != "completed":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail = "Invoice can only be created for completed appointment"
        )
    amount = new_invoice.total_amount
    invoice_in = Invoice(
        patient_id = appointment.patient_id,
        appointment_id = appointment.appointment_id,
        total_amount = amount)
    return manager.create_invoices(invoice_in,db)


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