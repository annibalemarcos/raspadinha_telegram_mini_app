from fastapi import APIRouter, Depends, Request, Form, File, UploadFile
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from sqlalchemy import func
from pathlib import Path
import uuid, json
from app.database import get_db
from app.models import User, ScratchCard, ScratchPrize, ScratchPlay, Transaction, AdminUser, AuditLog, Invoice, Payout
from app.security import verify_password, redirect_if_not_admin
from app.config import APP_NAME
from app.services.rtp_service import calculate_rtp, calculate_house_edge, expected_return_per_play, rule_label

router = APIRouter(prefix="/admin", tags=["admin"])
UPLOAD_DIR = Path("backend/app/static/uploads/covers")
ALLOWED_COVER_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}

def tpl(request: Request, name: str, context: dict):
    return request.app.state.templates.TemplateResponse(name, {"request": request, "app_name": APP_NAME, **context})

def save_cover_file(file: UploadFile | None) -> str | None:
    if not file or not file.filename: return None
    ext = Path(file.filename).suffix.lower()
    if ext not in ALLOWED_COVER_EXTENSIONS: return None
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
    filename = f"{uuid.uuid4().hex}{ext}"
    target = UPLOAD_DIR / filename
    content = file.file.read()
    if not content: return None
    target.write_bytes(content)
    return f"/static/uploads/covers/{filename}"

@router.get("", response_class=HTMLResponse)
def admin_root(request: Request): return RedirectResponse("/admin/dashboard", status_code=303)

@router.get("/login", response_class=HTMLResponse)
def login_page(request: Request): return tpl(request, "admin/login.html", {"error": None})

@router.post("/login")
def login(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    admin = db.query(AdminUser).filter(AdminUser.username == username, AdminUser.active == True).first()
    if not admin or not verify_password(password, admin.password_hash):
        return tpl(request, "admin/login.html", {"error": "Usuário ou senha inválidos"})
    request.session["admin"] = admin.username
    return RedirectResponse("/admin/dashboard", status_code=303)

@router.post("/logout")
def logout(request: Request):
    request.session.clear(); return RedirectResponse("/admin/login", status_code=303)

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request, db: Session = Depends(get_db)):
    redirect = redirect_if_not_admin(request)
    if redirect: return redirect
    users_count = db.query(User).count(); cards_count = db.query(ScratchCard).count(); plays_count = db.query(ScratchPlay).count()
    blocked_count = db.query(User).filter(User.status == "blocked").count(); invoices_count = db.query(Invoice).count()
    pending_invoices = db.query(Invoice).filter(Invoice.status == "pending").count()
    paid_invoices = db.query(Invoice).filter(Invoice.status.in_(["paid", "pix_confirmed", "played"])).count()
    canceled_invoices = db.query(Invoice).filter(Invoice.status == "canceled").count(); payouts_count = db.query(Payout).count()
    totals = db.query(func.coalesce(func.sum(Invoice.amount), 0), func.coalesce(func.sum(ScratchPlay.prize), 0)).first()
    total_invoice_amount = float(totals[0] or 0); total_prize = float(totals[1] or 0)
    rtp = round((total_prize / total_invoice_amount) * 100, 2) if total_invoice_amount > 0 else 0
    recent_invoices = db.query(Invoice).order_by(Invoice.created_at.desc()).limit(8).all()
    recent_plays = db.query(ScratchPlay).order_by(ScratchPlay.created_at.desc()).limit(8).all()
    return tpl(request, "admin/dashboard.html", locals())

@router.get("/users", response_class=HTMLResponse)
def users(request: Request, db: Session = Depends(get_db)):
    redirect = redirect_if_not_admin(request)
    if redirect: return redirect
    rows = db.query(User).order_by(User.created_at.desc()).all()
    return tpl(request, "admin/users.html", {"users": rows})

@router.post("/users/{user_id}/block")
def block_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    redirect = redirect_if_not_admin(request)
    if redirect: return redirect
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.status = "blocked"; db.add(AuditLog(actor=request.session.get("admin"), action="block_user", entity=f"user:{user.id}")); db.commit()
    return RedirectResponse("/admin/users", status_code=303)

@router.post("/users/{user_id}/unblock")
def unblock_user(request: Request, user_id: int, db: Session = Depends(get_db)):
    redirect = redirect_if_not_admin(request)
    if redirect: return redirect
    user = db.query(User).filter(User.id == user_id).first()
    if user:
        user.status = "active"; db.add(AuditLog(actor=request.session.get("admin"), action="unblock_user", entity=f"user:{user.id}")); db.commit()
    return RedirectResponse("/admin/users", status_code=303)

@router.get("/scratch-cards", response_class=HTMLResponse)
def scratch_cards(request: Request, db: Session = Depends(get_db)):
    redirect = redirect_if_not_admin(request)
    if redirect: return redirect
    cards = db.query(ScratchCard).order_by(ScratchCard.id.desc()).all()
    card_metrics = {c.id: {"rtp": calculate_rtp(c), "house_edge": calculate_house_edge(c), "expected_return": expected_return_per_play(c), "rule_label": rule_label(c.match_count)} for c in cards}
    return tpl(request, "admin/scratch_cards.html", {"cards": cards, "card_metrics": card_metrics})

@router.post("/scratch-cards")
def create_card(request: Request, name: str = Form(...), description: str = Form(""), price: float = Form(...), max_prize: float = Form(...), match_count: int = Form(3), cover_image: UploadFile | None = File(None), db: Session = Depends(get_db)):
    redirect = redirect_if_not_admin(request)
    if redirect: return redirect
    match_count = max(1, min(int(match_count or 3), 9)); cover_url = save_cover_file(cover_image)
    card = ScratchCard(name=name, description=description, price=price, max_prize=max_prize, rtp=0, match_count=match_count, cover_image=cover_url, active=True)
    db.add(card); db.commit(); db.refresh(card)
    demo_prizes = [(0,70,"Não foi dessa vez"),(price,15,"Reembolso"),(price*2,10,"Dobrou"),(min(max_prize,price*5),4,"Prêmio bom"),(max_prize,1,"Prêmio máximo")]
    for amount, probability, label in demo_prizes:
        db.add(ScratchPrize(scratch_card_id=card.id, prize_amount=float(amount), probability=float(probability), label=label))
    db.commit(); db.refresh(card)
    db.add(AuditLog(actor=request.session.get("admin"), action="create_card", entity=f"scratch_card:{card.id}", metadata_json=json.dumps({"match_count": match_count, "cover_image": cover_url, "rtp_calculated": calculate_rtp(card)}, ensure_ascii=False)))
    db.commit(); return RedirectResponse("/admin/scratch-cards", status_code=303)

@router.post("/scratch-cards/{card_id}/toggle")
def toggle_card(request: Request, card_id: int, db: Session = Depends(get_db)):
    redirect = redirect_if_not_admin(request)
    if redirect: return redirect
    card = db.query(ScratchCard).filter(ScratchCard.id == card_id).first()
    if card:
        card.active = not card.active; db.add(AuditLog(actor=request.session.get("admin"), action="toggle_card", entity=f"scratch_card:{card.id}")); db.commit()
    return RedirectResponse("/admin/scratch-cards", status_code=303)

@router.get("/invoices", response_class=HTMLResponse)
def invoices(request: Request, db: Session = Depends(get_db)):
    redirect = redirect_if_not_admin(request)
    if redirect: return redirect
    rows = db.query(Invoice).order_by(Invoice.created_at.desc()).limit(300).all(); return tpl(request, "admin/invoices.html", {"invoices": rows})

@router.get("/plays", response_class=HTMLResponse)
def plays(request: Request, db: Session = Depends(get_db)):
    redirect = redirect_if_not_admin(request)
    if redirect: return redirect
    rows = db.query(ScratchPlay).order_by(ScratchPlay.created_at.desc()).limit(300).all(); return tpl(request, "admin/plays.html", {"plays": rows})

@router.get("/payouts", response_class=HTMLResponse)
def payouts(request: Request, db: Session = Depends(get_db)):
    redirect = redirect_if_not_admin(request)
    if redirect: return redirect
    rows = db.query(Payout).order_by(Payout.created_at.desc()).limit(300).all(); return tpl(request, "admin/payouts.html", {"payouts": rows})

@router.get("/transactions", response_class=HTMLResponse)
def transactions(request: Request, db: Session = Depends(get_db)):
    redirect = redirect_if_not_admin(request)
    if redirect: return redirect
    rows = db.query(Transaction).order_by(Transaction.created_at.desc()).limit(300).all(); return tpl(request, "admin/transactions.html", {"transactions": rows})

@router.get("/audit-logs", response_class=HTMLResponse)
def audit_logs(request: Request, db: Session = Depends(get_db)):
    redirect = redirect_if_not_admin(request)
    if redirect: return redirect
    rows = db.query(AuditLog).order_by(AuditLog.created_at.desc()).limit(300).all(); return tpl(request, "admin/audit_logs.html", {"logs": rows})
