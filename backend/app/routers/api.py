from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
import json
from app.database import get_db
from app.models import User, ScratchCard, ScratchPlay
from app.services.invoice_service import InvoiceService
from app.services.scratch_engine import ScratchEngine
from app.services.rtp_service import calculate_rtp, calculate_house_edge, expected_return_per_play, rule_label

router = APIRouter(prefix="/api", tags=["api"])
class TelegramUserPayload(BaseModel):
    telegram_id: int; username: str | None = None; first_name: str | None = None
class InvoicePayload(BaseModel):
    telegram_id: int; scratch_card_id: int
class InvoiceActionPayload(BaseModel):
    telegram_id: int; invoice_id: int
class PixConfirmPayload(BaseModel):
    telegram_id: int; invoice_id: int; pix_key: str

@router.post("/telegram/user")
def create_or_get_user(payload: TelegramUserPayload, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.telegram_id == payload.telegram_id).first()
    if not user:
        user = User(telegram_id=payload.telegram_id, username=payload.username, first_name=payload.first_name, status="active")
        db.add(user); db.commit(); db.refresh(user)
    return {"id": user.id, "telegram_id": user.telegram_id, "username": user.username, "first_name": user.first_name, "status": user.status}

@router.get("/scratch-cards")
def list_cards(db: Session = Depends(get_db)):
    cards = db.query(ScratchCard).filter(ScratchCard.active == True).all()
    return [{"id": c.id, "name": c.name, "description": c.description, "price": c.price, "max_prize": c.max_prize, "match_count": c.match_count, "rule_label": rule_label(c.match_count), "cover_image": c.cover_image, "rtp": calculate_rtp(c), "house_edge": calculate_house_edge(c), "expected_return": expected_return_per_play(c)} for c in cards]

@router.post("/invoice/create")
def create_invoice(payload: InvoicePayload, db: Session = Depends(get_db)):
    try:
        invoice = InvoiceService.create_invoice(db, payload.telegram_id, payload.scratch_card_id)
        return {"id": invoice.id, "amount": invoice.amount, "status": invoice.status, "pix_code": invoice.pix_code, "scratch_card": invoice.scratch_card.name, "scratch_card_id": invoice.scratch_card_id}
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))

@router.post("/invoice/pay-demo")
def pay_invoice(payload: InvoiceActionPayload, db: Session = Depends(get_db)):
    try:
        invoice = InvoiceService.simulate_payment(db, payload.telegram_id, payload.invoice_id)
        return {"id": invoice.id, "amount": invoice.amount, "status": invoice.status, "scratch_card": invoice.scratch_card.name}
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))

@router.post("/invoice/confirm-pix")
def confirm_pix(payload: PixConfirmPayload, db: Session = Depends(get_db)):
    try:
        invoice = InvoiceService.confirm_player_pix(db, payload.telegram_id, payload.invoice_id, payload.pix_key)
        return {"id": invoice.id, "status": invoice.status, "player_pix_key": invoice.player_pix_key, "scratch_card": invoice.scratch_card.name, "amount": invoice.amount}
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))

@router.post("/invoice/cancel")
def cancel_invoice(payload: InvoiceActionPayload, db: Session = Depends(get_db)):
    try:
        invoice = InvoiceService.cancel_invoice(db, payload.telegram_id, payload.invoice_id)
        return {"id": invoice.id, "amount": invoice.amount, "status": invoice.status}
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))

@router.post("/play-paid")
def play_paid(payload: InvoiceActionPayload, db: Session = Depends(get_db)):
    try: return ScratchEngine.play_paid_invoice(db, payload.telegram_id, payload.invoice_id)
    except ValueError as e: raise HTTPException(status_code=400, detail=str(e))

@router.get("/history/{telegram_id}")
def history(telegram_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.telegram_id == telegram_id).first()
    if not user: raise HTTPException(status_code=404, detail="Usuário não encontrado")
    plays = db.query(ScratchPlay).filter(ScratchPlay.user_id == user.id).order_by(ScratchPlay.created_at.desc()).limit(20).all()
    return [{"id": p.id, "invoice_id": p.invoice_id, "card": p.scratch_card.name, "cost": p.cost, "prize": p.prize, "payout_status": p.payout_status, "match_count": p.match_count, "rule_label": rule_label(p.match_count), "pix_key": p.invoice.player_pix_key if p.invoice else None, "symbols": json.loads(p.symbols_json) if p.symbols_json else [], "result_hash": p.result_hash, "created_at": p.created_at.isoformat()} for p in plays]
