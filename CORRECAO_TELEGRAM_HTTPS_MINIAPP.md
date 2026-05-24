# Correção: Telegram Mini App exige HTTPS

Erro:

```txt
Bad Request: inline keyboard button Web App URL 'http://127.0.0.1:8000/app' is invalid: Only HTTPS links are allowed
```

## Causa

O Telegram não aceita `http://127.0.0.1` como URL de Mini App.

Mini Apps precisam usar URL pública com HTTPS.

## Como testar localmente

No navegador:

```txt
http://127.0.0.1:8000/app
```

## Como testar dentro do Telegram

Use ngrok:

```powershell
ngrok http 8000
```

Copie a URL HTTPS e coloque no `.env`:

```env
MINI_APP_URL=https://sua-url-ngrok.ngrok-free.app/app
API_BASE_URL=https://sua-url-ngrok.ngrok-free.app
```

Depois reinicie backend e bot.

## O que este ZIP muda

O `bot.py` agora verifica se `MINI_APP_URL` começa com `https://`.

- Se for HTTPS: cria botão WebApp.
- Se não for HTTPS: mostra aviso e evita quebrar o bot.
