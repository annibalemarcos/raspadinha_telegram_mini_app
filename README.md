# 🎟️ Raspadinha Telegram — Mini App Demo

MVP de raspadinha em **Telegram Mini App**, com animação visual de raspar usando `canvas`.

> Tudo é fictício: Pix fake, pagamento fake e payout fake.

## Fluxo

```txt
/start no bot
  ↓
Abrir Mini App
  ↓
Escolher raspadinha
  ↓
Criar invoice Pix fake
  ↓
Simular pagamento
  ↓
Inserir chave Pix
  ↓
Confirmar chave Pix
  ↓
Raspar a tela
  ↓
Resultado visual
  ↓
Se ganhar: payout demo automático
```

## Rodar no Windows

```powershell
cd raspadinha_telegram
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
pip install -r backend\requirements.txt
pip install -r bot\requirements.txt
copy .env.example .env
del raspadinha.db
python scripts\seed_demo.py
python backend\run.py
```

Abra:

```txt
http://127.0.0.1:8000/app
```

Admin:

```txt
http://127.0.0.1:8000/admin
admin / admin123
```

## Bot

Edite `.env`:

```env
TELEGRAM_BOT_TOKEN=SEU_TOKEN
MINI_APP_URL=http://127.0.0.1:8000/app
```

Rode:

```powershell
python bot\bot.py
```

## Telegram real precisa HTTPS

Para abrir como Mini App dentro do Telegram, use URL pública HTTPS.

Exemplo:

```powershell
ngrok http 8000
```

Depois coloque no `.env`:

```env
MINI_APP_URL=https://sua-url-ngrok.ngrok-free.app/app
API_BASE_URL=https://sua-url-ngrok.ngrok-free.app
```


## Corrigir Internal Server Error no login admin

Esta versão remove `passlib/bcrypt` do login admin e usa hash nativo com `hashlib`.

Se der erro ao logar, resete o banco:

```powershell
del raspadinha.db
python scripts\seed_demo.py
python backend\run.py
```

Ou rode:

```bat
resetar_banco_e_rodar.bat
```


## Telegram Mini App exige HTTPS

Se aparecer:

```txt
Bad Request: inline keyboard button Web App URL 'http://127.0.0.1:8000/app' is invalid: Only HTTPS links are allowed
```

é porque o Telegram não aceita `http://127.0.0.1` como Web App.

Para testar local no navegador:

```txt
http://127.0.0.1:8000/app
```

Para testar dentro do Telegram:

```powershell
ngrok http 8000
```

Depois coloque no `.env`:

```env
MINI_APP_URL=https://sua-url-ngrok.ngrok-free.app/app
API_BASE_URL=https://sua-url-ngrok.ngrok-free.app
```

Reinicie o backend e o bot.


## Regras configuráveis

Agora o admin pode criar raspadinhas com regras diferentes:

```txt
1 símbolo ganha
2 iguais ganha
3 iguais ganha
4 iguais ganha
5 iguais ganha
6 iguais ganha
9 iguais ganha
```

No admin:

```txt
/admin/scratch-cards
```

Escolha o campo:

```txt
Regra de vitória
```

Como mudou a estrutura do banco, apague o SQLite antigo:

```powershell
del raspadinha.db
python scripts\seed_demo.py
python backend\run.py
```


## Atualização: RTP automático + capas/temas

Agora o admin não digita RTP na mão. O sistema calcula automaticamente usando:

```txt
preço da raspadinha + valor dos prêmios + probabilidade de cada prêmio
```

Também dá para enviar uma capa/tema da raspadinha no cadastro:

```txt
/admin/scratch-cards
```

Formatos aceitos:

```txt
PNG, JPG, JPEG, WEBP, GIF
```

Como mudou o banco:

```powershell
del raspadinha.db
python scripts\seed_demo.py
python backend\run.py
```


## Capa opcional com tema automático

No admin, o campo de capa é opcional.

```txt
/admin/scratch-cards
```

Se você enviar uma imagem, o Mini App usa a imagem enviada.

Se você não enviar nada, o Mini App escolhe automaticamente um tema visual baseado no ID da raspadinha:

```txt
💎 diamante
🔥 fogo
🍀 sorte
👑 rei
🪙 moeda
⭐ estrela
🎰 cassino
🌈 arco-íris
```

Assim nenhuma raspadinha fica feia ou vazia.
