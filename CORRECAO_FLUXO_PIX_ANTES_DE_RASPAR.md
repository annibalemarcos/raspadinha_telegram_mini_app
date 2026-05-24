# Correção de fluxo

Antes estava assim:

```txt
paga → raspa → se ganhar, pede Pix
```

Agora está correto:

```txt
paga → pede Pix → confirma Pix → libera raspadinha → se ganhar, payout fake automático
```

## Arquivos alterados

- `backend/app/models.py`
- `backend/app/services/invoice_service.py`
- `backend/app/services/scratch_engine.py`
- `backend/app/routers/api.py`
- `backend/app/templates/admin/invoices.html`
- `bot/bot.py`
- `docs/regras.md`
- `README.md`

## Atenção

Como mudou a estrutura do banco, apague o SQLite antigo antes de rodar:

```powershell
del raspadinha.db
python scripts\seed_demo.py
python backend\run.py
```
