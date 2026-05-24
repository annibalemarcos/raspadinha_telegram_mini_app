# Correção aplicada

O erro:

```txt
sqlalchemy.exc.InvalidRequestError: Attribute name 'metadata' is reserved when using the Declarative API.
```

acontecia porque `metadata` é nome reservado no SQLAlchemy Declarative API.

## Arquivos corrigidos

- `backend/app/models.py`
- `backend/app/services/scratch_engine.py`
- `backend/app/routers/admin.py`
- `backend/app/templates/admin/audit_logs.html`

## O que mudou

A coluna/campo `metadata` virou:

```python
metadata_json
```

Agora rode novamente:

```powershell
python scripts\seed_demo.py
python backend\run.py
```
