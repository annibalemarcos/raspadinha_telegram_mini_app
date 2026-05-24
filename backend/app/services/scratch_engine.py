import hashlib
import json
import random
import time
from sqlalchemy.orm import Session
from app.models import User, ScratchCard, ScratchPrize, ScratchPlay, Invoice, Transaction, AuditLog, Payout

class ScratchEngine:
    SYMBOLS = ["🍒", "🍋", "💎", "⭐", "7️⃣", "🍀", "🔔", "👑", "🍉", "🔥", "💰", "🪙"]

    @staticmethod
    def choose_prize(prizes: list[ScratchPrize]) -> ScratchPrize | None:
        total = sum(p.probability for p in prizes)
        if total <= 0:
            return None

        roll = random.uniform(0, total)
        cumulative = 0
        for prize in prizes:
            cumulative += prize.probability
            if roll <= cumulative:
                return prize
        return prizes[-1] if prizes else None

    @classmethod
    def generate_symbols(cls, won: bool, match_count: int):
        match_count = max(1, min(int(match_count or 3), 9))

        # Regra "1 ganha": qualquer símbolo revelado já é vitória.
        # Visualmente preenchemos a grade normalmente.
        if match_count == 1:
            return [random.choice(cls.SYMBOLS) for _ in range(9)]

        if won:
            symbol = random.choice(cls.SYMBOLS)
            others_pool = [s for s in cls.SYMBOLS if s != symbol]
            grid = [symbol] * match_count

            while len(grid) < 9:
                grid.append(random.choice(others_pool))

            random.shuffle(grid)
            return grid

        # Perdedor: garante que nenhum símbolo apareça match_count vezes ou mais.
        attempts = 0
        while True:
            attempts += 1
            grid = [random.choice(cls.SYMBOLS) for _ in range(9)]
            counts = {s: grid.count(s) for s in set(grid)}
            if max(counts.values()) < match_count:
                return grid

            # fallback para regras mais difíceis tipo 4, 5...
            if attempts > 500:
                grid = []
                idx = 0
                while len(grid) < 9:
                    symbol = cls.SYMBOLS[idx % len(cls.SYMBOLS)]
                    if grid.count(symbol) < match_count - 1:
                        grid.append(symbol)
                    idx += 1
                random.shuffle(grid)
                return grid

    @staticmethod
    def result_hash(payload: dict) -> str:
        raw = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(raw.encode("utf-8")).hexdigest()

    @classmethod
    def play_paid_invoice(cls, db: Session, telegram_id: int, invoice_id: int):
        user = db.query(User).filter(User.telegram_id == telegram_id).first()
        if not user:
            raise ValueError("Usuário não encontrado")
        if user.status != "active":
            raise ValueError("Usuário bloqueado")

        invoice = db.query(Invoice).filter(Invoice.id == invoice_id, Invoice.user_id == user.id).first()
        if not invoice:
            raise ValueError("Invoice não encontrada")
        if invoice.status != "pix_confirmed":
            raise ValueError(
                f"Antes de raspar, a invoice precisa estar paga e com chave Pix confirmada. Status atual: {invoice.status}"
            )
        if not invoice.player_pix_key:
            raise ValueError("Chave Pix do jogador ainda não foi confirmada")

        existing_play = db.query(ScratchPlay).filter(ScratchPlay.invoice_id == invoice.id).first()
        if existing_play:
            raise ValueError("Essa invoice já foi usada em uma jogada")

        card = db.query(ScratchCard).filter(ScratchCard.id == invoice.scratch_card_id, ScratchCard.active == True).first()
        if not card:
            raise ValueError("Raspadinha não encontrada ou inativa")

        match_count = max(1, min(int(card.match_count or 3), 9))

        prize = cls.choose_prize(card.prizes)
        prize_amount = float(prize.prize_amount if prize else 0.0)
        won = prize_amount > 0
        symbols = cls.generate_symbols(won, match_count)

        payload = {
            "telegram_id": telegram_id,
            "invoice_id": invoice.id,
            "player_pix_key": invoice.player_pix_key,
            "card_id": card.id,
            "card_name": card.name,
            "cost": card.price,
            "prize": prize_amount,
            "match_count": match_count,
            "symbols": symbols,
            "ts": time.time(),
            "nonce": random.randint(100000, 999999999)
        }
        rhash = cls.result_hash(payload)

        payout_status = "paid_demo" if won else "not_applicable"

        play = ScratchPlay(
            user_id=user.id,
            scratch_card_id=card.id,
            invoice_id=invoice.id,
            cost=card.price,
            prize=prize_amount,
            result_hash=rhash,
            symbols_json=json.dumps(symbols, ensure_ascii=False),
            match_count=match_count,
            status="completed",
            payout_status=payout_status
        )
        db.add(play)
        db.flush()

        invoice.status = "played"

        db.add(Transaction(
            user_id=user.id,
            type="scratch_play_demo",
            amount=card.price,
            status="completed",
            reference=f"Jogada demo invoice #{invoice.id} - {card.name}"
        ))

        payout_data = None
        if won:
            payout = Payout(
                user_id=user.id,
                scratch_play_id=play.id,
                amount=prize_amount,
                pix_key=invoice.player_pix_key,
                status="paid_demo",
                provider_reference=f"PIX-DEMO-PAYOUT-{play.id}-{random.randint(100000, 999999)}"
            )
            db.add(payout)
            db.flush()

            db.add(Transaction(
                user_id=user.id,
                type="payout_paid_demo",
                amount=prize_amount,
                status="completed",
                reference=f"Payout demo automático jogada #{play.id}"
            ))

            payout_data = {
                "id": payout.id,
                "amount": payout.amount,
                "pix_key": payout.pix_key,
                "status": payout.status,
                "provider_reference": payout.provider_reference
            }

        db.add(AuditLog(
            actor=str(telegram_id),
            action="scratch_play",
            entity=f"scratch_card:{card.id}",
            metadata_json=json.dumps(payload, ensure_ascii=False)
        ))

        if payout_data:
            db.add(AuditLog(
                actor=str(telegram_id),
                action="payout_paid_demo_auto",
                entity=f"play:{play.id}",
                metadata_json=json.dumps(payout_data, ensure_ascii=False)
            ))

        db.commit()
        db.refresh(play)

        return {
            "play_id": play.id,
            "invoice_id": invoice.id,
            "card": card.name,
            "cost": card.price,
            "prize": prize_amount,
            "match_count": match_count,
            "rule_label": "1 símbolo ganha" if match_count == 1 else f"{match_count} iguais ganha",
            "symbols": symbols,
            "result_hash": rhash,
            "won": won,
            "payout_status": payout_status,
            "player_pix_key": invoice.player_pix_key,
            "payout": payout_data
        }
