from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, ForeignKey, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    telegram_id = Column(Integer, unique=True, nullable=False, index=True)
    username = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    status = Column(String(50), default="active")
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow)
    invoices = relationship("Invoice", back_populates="user")
    plays = relationship("ScratchPlay", back_populates="user")
    transactions = relationship("Transaction", back_populates="user")
    payouts = relationship("Payout", back_populates="user")

class ScratchCard(Base):
    __tablename__ = "scratch_cards"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    price = Column(Float, nullable=False)
    max_prize = Column(Float, nullable=False)
    rtp = Column(Float, default=0.0)  # legado; agora o app calcula automaticamente
    match_count = Column(Integer, default=3)
    cover_image = Column(String(500), nullable=True)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    prizes = relationship("ScratchPrize", back_populates="scratch_card", cascade="all, delete-orphan")
    plays = relationship("ScratchPlay", back_populates="scratch_card")
    invoices = relationship("Invoice", back_populates="scratch_card")

class ScratchPrize(Base):
    __tablename__ = "scratch_prizes"
    id = Column(Integer, primary_key=True, index=True)
    scratch_card_id = Column(Integer, ForeignKey("scratch_cards.id"), nullable=False)
    prize_amount = Column(Float, nullable=False)
    probability = Column(Float, nullable=False)
    label = Column(String(255), nullable=True)
    scratch_card = relationship("ScratchCard", back_populates="prizes")

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scratch_card_id = Column(Integer, ForeignKey("scratch_cards.id"), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(50), default="pending")
    pix_code = Column(Text, nullable=True)
    player_pix_key = Column(String(255), nullable=True)
    pix_confirmed_at = Column(DateTime, nullable=True)
    paid_at = Column(DateTime, nullable=True)
    canceled_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="invoices")
    scratch_card = relationship("ScratchCard", back_populates="invoices")
    play = relationship("ScratchPlay", back_populates="invoice", uselist=False)

class ScratchPlay(Base):
    __tablename__ = "scratch_plays"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scratch_card_id = Column(Integer, ForeignKey("scratch_cards.id"), nullable=False)
    invoice_id = Column(Integer, ForeignKey("invoices.id"), nullable=True)
    cost = Column(Float, nullable=False)
    prize = Column(Float, default=0.0)
    result_hash = Column(String(128), nullable=True)
    symbols_json = Column(Text, nullable=True)
    match_count = Column(Integer, default=3)
    status = Column(String(50), default="completed")
    payout_status = Column(String(50), default="not_applicable")
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="plays")
    scratch_card = relationship("ScratchCard", back_populates="plays")
    invoice = relationship("Invoice", back_populates="play")
    payout = relationship("Payout", back_populates="play", uselist=False)

class Payout(Base):
    __tablename__ = "payouts"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    scratch_play_id = Column(Integer, ForeignKey("scratch_plays.id"), nullable=False)
    amount = Column(Float, nullable=False)
    pix_key = Column(String(255), nullable=False)
    status = Column(String(50), default="paid_demo")
    provider_reference = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="payouts")
    play = relationship("ScratchPlay", back_populates="payout")

class Transaction(Base):
    __tablename__ = "transactions"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    type = Column(String(50), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(50), default="completed")
    reference = Column(String(255), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    user = relationship("User", back_populates="transactions")

class AdminUser(Base):
    __tablename__ = "admin_users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"
    id = Column(Integer, primary_key=True, index=True)
    actor = Column(String(255), nullable=True)
    action = Column(String(255), nullable=False)
    entity = Column(String(255), nullable=True)
    metadata_json = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
