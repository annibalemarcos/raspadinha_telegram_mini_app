from app.models import ScratchCard

def calculate_rtp(card: ScratchCard) -> float:
    if not card or not card.price or card.price <= 0:
        return 0.0
    expected_return = 0.0
    for prize in card.prizes or []:
        expected_return += float(prize.prize_amount or 0) * (float(prize.probability or 0) / 100.0)
    return round((expected_return / float(card.price)) * 100.0, 2)

def calculate_house_edge(card: ScratchCard) -> float:
    return round(100.0 - calculate_rtp(card), 2)

def expected_return_per_play(card: ScratchCard) -> float:
    if not card:
        return 0.0
    value = 0.0
    for prize in card.prizes or []:
        value += float(prize.prize_amount or 0) * (float(prize.probability or 0) / 100.0)
    return round(value, 2)

def rule_label(match_count: int) -> str:
    try:
        match_count = int(match_count or 3)
    except Exception:
        match_count = 3
    return "1 símbolo ganha" if match_count == 1 else f"{match_count} iguais ganha"
