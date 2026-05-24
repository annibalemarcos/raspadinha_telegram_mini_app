# Correção: SyntaxError no bot.py

Erro:

```txt
SyntaxError: unterminated string literal
```

Causa: uma string estava com aspas quebradas.

## Arquivo corrigido

```txt
bot/bot.py
```

## Teste

```powershell
python -m py_compile bot\bot.py
python bot\bot.py
```
