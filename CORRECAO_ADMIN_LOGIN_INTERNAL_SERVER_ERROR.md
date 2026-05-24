# Correção: Internal Server Error no login admin

Foi removida a dependência de `passlib/bcrypt` no login admin.

Agora o hash de senha usa apenas biblioteca nativa do Python:

```python
hashlib.pbkdf2_hmac
```

## Por que isso ajuda?

No Windows, `passlib + bcrypt` pode quebrar ou gerar erro interno dependendo da versão instalada.

## Como aplicar

Como o formato da senha mudou, apague o banco antigo e rode o seed:

```powershell
del raspadinha.db
python scripts\seed_demo.py
python backend\run.py
```

Ou use:

```bat
resetar_banco_e_rodar.bat
```

Login:

```txt
admin
admin123
```
