import random, string
from datetime import datetime
from sqlalchemy.orm import Session
from app.models import User, ScratchCard, Invoice, Transaction, AuditLog

class InvoiceService:
    @staticmethod
    def fake_pix_code(invoice_id: int, amount: float) -> str:
        suffix = ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(18))
        return f"PIX-DEMO-INVOICE-{invoice_id}-VALOR-{amount:.2f}-{suffix}"

    @classmethod
    def create_invoice(cls, db: Session, telegram_id: int, scratch_card_id: int):
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if not user: raise ValueError('Usuário não encontrado')
        if user.status != 'active': raise ValueError('Usuário bloqueado')
        card = db.query(ScratchCard).filter(ScratchCard.id == scratch_card_id, ScratchCard.active == True).first()
        if not card: raise ValueError('Raspadinha não encontrada ou inativa')
        invoice = Invoice(user_id=user.id, scratch_card_id=card.id, amount=card.price, status='pending', pix_code='GERANDO...')
        db.add(invoice); db.commit(); db.refresh(invoice)
        invoice.pix_code = cls.fake_pix_code(invoice.id, invoice.amount)
        db.add(Transaction(user_id=user.id, type='invoice_created', amount=invoice.amount, status='pending', reference=f'Invoice demo #{invoice.id} - {card.name}'))
        db.add(AuditLog(actor=str(telegram_id), action='invoice_created', entity=f'invoice:{invoice.id}', metadata_json=f'scratch_card_id={card.id};amount={invoice.amount}'))
        db.commit(); db.refresh(invoice)
        return invoice

    @staticmethod
    def simulate_payment(db: Session, telegram_id: int, invoice_id: int):
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if not user: raise ValueError('Usuário não encontrado')
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id, Invoice.user_id == user.id).first()
        if not invoice: raise ValueError('Invoice não encontrada')
        if invoice.status != 'pending': raise ValueError(f'Invoice não está pendente. Status atual: {invoice.status}')
        invoice.status = 'paid'; invoice.paid_at = datetime.utcnow()
        db.add(Transaction(user_id=user.id, type='invoice_paid_demo', amount=invoice.amount, status='completed', reference=f'Pagamento demo invoice #{invoice.id}'))
        db.add(AuditLog(actor=str(telegram_id), action='invoice_paid_demo', entity=f'invoice:{invoice.id}', metadata_json=f'amount={invoice.amount}'))
        db.commit(); db.refresh(invoice)
        return invoice

    @staticmethod
    def confirm_player_pix(db: Session, telegram_id: int, invoice_id: int, pix_key: str):
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if not user: raise ValueError('Usuário não encontrado')
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id, Invoice.user_id == user.id).first()
        if not invoice: raise ValueError('Invoice não encontrada')
        if invoice.status != 'paid': raise ValueError(f'Para confirmar Pix, a invoice precisa estar paga. Status atual: {invoice.status}')
        pix_key = (pix_key or '').strip()
        if len(pix_key) < 3: raise ValueError('Chave Pix inválida ou curta demais')
        invoice.player_pix_key = pix_key; invoice.pix_confirmed_at = datetime.utcnow(); invoice.status = 'pix_confirmed'
        db.add(Transaction(user_id=user.id, type='player_pix_confirmed', amount=0, status='completed', reference=f'Chave Pix confirmada para invoice #{invoice.id}'))
        db.add(AuditLog(actor=str(telegram_id), action='player_pix_confirmed', entity=f'invoice:{invoice.id}', metadata_json=f'pix_key={pix_key}'))
        db.commit(); db.refresh(invoice)
        return invoice

    @staticmethod
    def cancel_invoice(db: Session, telegram_id: int, invoice_id: int):
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if not user: raise ValueError('Usuário não encontrado')
        invoice = db.query(Invoice).filter(Invoice.id == invoice_id, Invoice.user_id == user.id).first()
        if not invoice: raise ValueError('Invoice não encontrada')
        if invoice.status not in ['pending','paid']: raise ValueError(f'Invoice não pode ser cancelada. Status atual: {invoice.status}')
        invoice.status = 'canceled'; invoice.canceled_at = datetime.utcnow()
        db.add(Transaction(user_id=user.id, type='invoice_canceled', amount=invoice.amount, status='canceled', reference=f'Cancelamento invoice #{invoice.id}'))
        db.add(AuditLog(actor=str(telegram_id), action='invoice_canceled', entity=f'invoice:{invoice.id}', metadata_json=f'amount={invoice.amount}'))
        db.commit(); db.refresh(invoice)
        return invoice
