import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
sys.path.insert(0, str(BACKEND))
from app.database import Base, engine, SessionLocal
from app.models import AdminUser, ScratchCard, ScratchPrize
from app.security import hash_password
from app.config import ADMIN_USERNAME, ADMIN_PASSWORD
from app.services.rtp_service import calculate_rtp

def create_card(db, name, description, price, max_prize, prizes, match_count=3, cover_image=None):
    card = db.query(ScratchCard).filter(ScratchCard.name == name).first()
    if card: return card
    card = ScratchCard(name=name, description=description, price=price, max_prize=max_prize, rtp=0, match_count=match_count, cover_image=cover_image, active=True)
    db.add(card); db.commit(); db.refresh(card)
    for amount, probability, label in prizes:
        db.add(ScratchPrize(scratch_card_id=card.id, prize_amount=amount, probability=probability, label=label))
    db.commit(); db.refresh(card)
    print(f"🎟️ {name} criada | RTP calculado: {calculate_rtp(card)}%")
    return card

def main():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        admin = db.query(AdminUser).filter(AdminUser.username == ADMIN_USERNAME).first()
        if not admin:
            admin = AdminUser(username=ADMIN_USERNAME, password_hash=hash_password(ADMIN_PASSWORD), active=True)
            db.add(admin); db.commit(); print(f"✅ Admin criado: {ADMIN_USERNAME} / {ADMIN_PASSWORD}")
        else: print("ℹ️ Admin já existe.")
        create_card(db, "Bronze Demo", "Baratinha, rápida e sem drama.", 1.0, 10.0, [(0.0,70,"Nada"),(1.0,15,"Reembolso"),(2.0,10,"Dobrou"),(5.0,4,"Boa!"),(10.0,1,"Máximo")], match_count=3)
        create_card(db, "Prata Demo", "Mais risco, mais brilho.", 2.0, 25.0, [(0.0,68,"Nada"),(2.0,16,"Reembolso"),(4.0,10,"Dobrou"),(10.0,5,"Boa!"),(25.0,1,"Máximo")], match_count=4)
        create_card(db, "Ouro Demo", "A bonita perigosa. Só demo, calma.", 5.0, 100.0, [(0.0,65,"Nada"),(5.0,17,"Reembolso"),(10.0,10,"Dobrou"),(25.0,6,"Boa!"),(100.0,2,"Máximo")], match_count=1)
        print("✅ Raspadinhas demo criadas."); print("✅ Seed finalizado.")
    finally: db.close()
if __name__ == "__main__": main()
