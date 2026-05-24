# Correção: regras 1, 3, 4 iguais ganha

Agora cada raspadinha possui:

```python
match_count
```

Exemplos:

```txt
1 → 1 símbolo ganha
3 → 3 iguais ganha
4 → 4 iguais ganha
```

## Arquivos alterados

- `backend/app/models.py`
- `backend/app/services/scratch_engine.py`
- `backend/app/routers/admin.py`
- `backend/app/routers/api.py`
- `backend/app/templates/admin/scratch_cards.html`
- `backend/app/templates/admin/plays.html`
- `backend/app/static/miniapp/app.js`
- `backend/app/static/miniapp/app.css`
- `scripts/seed_demo.py`

## Atenção

Como mudou banco, rode:

```powershell
del raspadinha.db
python scripts\seed_demo.py
python backend\run.py
```
