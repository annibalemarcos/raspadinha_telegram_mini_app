# 🎟️ Raspadinha Telegram Mini App — Demo MVP

MVP de uma plataforma de **raspadinha em Telegram Mini App**, com backend em **FastAPI**, painel administrativo, bot em **aiogram**, animação visual de raspadinha com **Canvas**, invoice Pix fictícia, chave Pix antes da raspagem, RTP automático e capas/temas customizáveis.

> ⚠️ **Projeto demonstrativo/fictício.**
>
> Este projeto não processa dinheiro real, não faz Pix real, não faz payout real e não deve ser usado em produção com apostas/jogos de azar sem análise jurídica, licença, compliance, KYC, antifraude e auditoria.

---z

## ✨ Visão geral

O sistema simula o fluxo completo de uma raspadinha dentro do Telegram:

```txt
Usuário abre o bot
↓
Clica em “Abrir Mini App”
↓
Escolhe uma raspadinha
↓
Gera invoice Pix demo
↓
Simula pagamento
↓
Informa e confirma chave Pix
↓
Raspa a tela com animação
↓
Recebe resultado
↓
Se ganhar, payout demo é registrado automaticamente
```

---

## 🚀 Principais recursos

- Bot Telegram com botão para abrir Mini App.
- Mini App responsivo em `/app`.
- Animação real de raspadinha usando `canvas`.
- Painel administrativo web.
- Cadastro de raspadinhas.
- Regra de vitória configurável:
  - `1 símbolo ganha`
  - `2 iguais ganha`
  - `3 iguais ganha`
  - `4 iguais ganha`
  - `5 iguais ganha`
  - `6 iguais ganha`
  - `9 iguais ganha`
- Upload opcional de capa/tema da raspadinha.
- Tema automático caso nenhuma capa seja enviada.
- RTP calculado automaticamente.
- Invoice Pix fictícia.
- Chave Pix do jogador antes da raspagem.
- Registro de jogadas.
- Registro de payouts demo.
- Registro de transações demo.
- Logs de auditoria.
- SQLite para desenvolvimento local.
- Estrutura simples para subir em Render, Railway, VPS ou similar.

---

## 🧱 Stack

| Camada | Tecnologia |
|---|---|
| Backend | FastAPI |
| Banco | SQLite |
| ORM | SQLAlchemy |
| Templates | Jinja2 |
| Admin UI | Bootstrap |
| Bot Telegram | aiogram |
| Mini App | HTML, CSS, JavaScript |
| Animação | Canvas API |
| Configuração | `.env` / python-dotenv |

---

## 📁 Estrutura do projeto

```txt
raspadinha_telegram/
├── backend/
│   ├── app/
│   │   ├── routers/
│   │   ├── services/
│   │   ├── static/
│   │   │   ├── miniapp/
│   │   │   └── uploads/
│   │   │       └── covers/
│   │   ├── templates/
│   │   │   ├── admin/
│   │   │   └── miniapp/
│   │   ├── models.py
│   │   ├── database.py
│   │   ├── main.py
│   │   └── security.py
│   ├── requirements.txt
│   └── run.py
│
├── bot/
│   ├── bot.py
│   └── requirements.txt
│
├── scripts/
│   └── seed_demo.py
│
├── docs/
├── .env.example
├── README.md
└── reinstalar_tudo.bat
```

---

## ⚙️ Instalação local

### 1. Clone o repositório

```powershell
git clone https://github.com/SEU_USUARIO/raspadinha-telegram-mini-app.git
cd raspadinha-telegram-mini-app
```

Ou, se você ainda não subiu para o GitHub, entre na pasta onde extraiu o ZIP:

```powershell
cd C:\my_projects\raspadinha_telegram_mini_app
```

---

### 2. Crie o ambiente virtual

```powershell
python -m venv .venv
.venv\Scripts\activate
```

Se estiver no PowerShell e der bloqueio de execução, rode:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.venv\Scripts\activate
```

---

### 3. Instale as dependências

```powershell
python -m pip install --upgrade pip setuptools wheel
pip install -r backend\requirements.txt
pip install -r bot\requirements.txt
```

---

### 4. Configure o `.env`

Copie o exemplo:

```powershell
copy .env.example .env
```

Edite o `.env`:

```env
APP_NAME=Raspadinha Telegram Mini App Demo
SECRET_KEY=troque-esta-chave
DATABASE_URL=sqlite:///./raspadinha.db

ADMIN_USERNAME=admin
ADMIN_PASSWORD=admin123

TELEGRAM_BOT_TOKEN=SEU_TOKEN_DO_BOT

API_BASE_URL=http://127.0.0.1:8000
MINI_APP_URL=http://127.0.0.1:8000/app
```

---

### 5. Crie o banco demo

```powershell
python scripts\seed_demo.py
```

Se você já rodou versões antigas e quer resetar tudo:

```powershell
del raspadinha.db
python scripts\seed_demo.py
```

---

## ▶️ Rodando o backend

```powershell
python backend\run.py
```

Acesse:

```txt
http://127.0.0.1:8000
```

Mini App local:

```txt
http://127.0.0.1:8000/app
```

Admin:

```txt
http://127.0.0.1:8000/admin/login
```

Login padrão:

```txt
admin
admin123
```

---

## 🤖 Rodando o bot

Em outro terminal:

```powershell
cd C:\my_projects\raspadinha_telegram_mini_app
.venv\Scripts\activate
python bot\bot.py
```

Se estiver tudo certo, aparecerá algo como:

```txt
🤖 Bot rodando com Telegram Mini App...
Mini App URL: http://127.0.0.1:8000/app
```

---

## 🌐 Usando o Mini App dentro do Telegram

O Telegram **não aceita** `http://127.0.0.1` como Mini App real.

Para abrir dentro do Telegram, a URL precisa ser pública e HTTPS.

### Usando ngrok

Com o backend rodando na porta `8000`, abra outro terminal:

```powershell
ngrok http 8000
```

O ngrok vai gerar uma URL parecida com:

```txt
https://abc123.ngrok-free.app
```

Atualize o `.env`:

```env
API_BASE_URL=https://abc123.ngrok-free.app
MINI_APP_URL=https://abc123.ngrok-free.app/app
```

Depois reinicie o bot:

```powershell
python bot\bot.py
```

Ordem recomendada dos terminais:

```txt
Terminal 1 → python backend\run.py
Terminal 2 → ngrok http 8000
Terminal 3 → python bot\bot.py
```

---

## 🎟️ Como criar raspadinhas

No admin:

```txt
/admin/scratch-cards
```

Você pode configurar:

- Nome.
- Descrição.
- Capa/tema.
- Preço.
- Prêmio máximo.
- Regra de vitória.

Exemplos de regra:

```txt
1 símbolo ganha
3 iguais ganha
4 iguais ganha
```

---

## 🖼️ Capas e temas

O campo de capa é opcional.

Se você enviar uma imagem, o Mini App usa essa capa.

Se você não enviar nada, o sistema aplica automaticamente um tema visual.

Temas automáticos disponíveis:

```txt
💎 Diamante
🔥 Fogo
🍀 Sorte
👑 Rei
🪙 Moeda
⭐ Estrela
🎰 Cassino
🌈 Arco-íris
```

Formatos aceitos para upload:

```txt
PNG
JPG
JPEG
WEBP
GIF
```

As capas ficam em:

```txt
backend/app/static/uploads/covers/
```

---

## 📊 RTP automático

O admin **não digita RTP manualmente**.

O sistema calcula o RTP com base em:

```txt
preço da raspadinha
valor dos prêmios
probabilidade de cada prêmio
```

Fórmula simplificada:

```txt
RTP = retorno médio esperado / preço da raspadinha
```

Exemplo:

```txt
Preço da raspadinha: R$ 1,00
Retorno médio esperado: R$ 0,65
RTP calculado: 65%
Margem teórica: 35%
```

No admin, o sistema exibe:

- RTP calculado.
- Retorno médio por jogada.
- Margem teórica.

---

## 🧪 Fluxo demo do jogo

1. Usuário entra no bot.
2. Abre o Mini App.
3. Escolhe uma raspadinha.
4. Sistema cria invoice Pix fictícia.
5. Usuário clica em “Simular pagamento”.
6. Usuário informa e confirma chave Pix.
7. A raspadinha é liberada.
8. Usuário raspa a tela.
9. O resultado aparece.
10. Se ganhar, o payout demo é registrado no admin.

---

## 🔐 Segurança e limitações

Este projeto é um MVP técnico.

Ele **não possui**:

- Pix real.
- Gateway de pagamento real.
- Saque real.
- Antifraude real.
- KYC.
- Auditoria criptográfica completa.
- Controle regulatório.
- Licenciamento jurídico.
- Proteção para produção.

Antes de qualquer uso real, seria necessário implementar:

- Compliance.
- Termos de uso.
- Política de privacidade.
- Logs imutáveis.
- Auditoria de sorteio.
- Rate limit.
- Proteção contra abuso.
- Validação real de pagamento.
- Integração com provedor financeiro autorizado.
- Segurança de sessão.
- Deploy com HTTPS.
- Backups.
- Monitoramento.

---

## 🧹 Arquivos que não devem ir para o GitHub

Use um `.gitignore` assim:

```gitignore
.venv/
venv/
__pycache__/
*.pyc

.env
raspadinha.db

backend/app/static/uploads/covers/*
!backend/app/static/uploads/covers/.gitkeep

.DS_Store
Thumbs.db
```

Nunca suba:

```txt
.env
raspadinha.db
.venv/
```

O arquivo correto para subir é:

```txt
.env.example
```

---

## 🛠️ Comandos úteis

Resetar banco:

```powershell
del raspadinha.db
python scripts\seed_demo.py
```

Rodar backend:

```powershell
python backend\run.py
```

Rodar bot:

```powershell
python bot\bot.py
```

Testar Mini App local:

```txt
http://127.0.0.1:8000/app
```

Testar admin:

```txt
http://127.0.0.1:8000/admin/login
```

---

## 🚀 Subindo para o GitHub

```powershell
git init
git branch -M main
git add .
git commit -m "Initial Telegram mini app scratch card MVP"
git remote add origin https://github.com/SEU_USUARIO/raspadinha-telegram-mini-app.git
git push -u origin main
```

---

## 📌 Status do projeto

```txt
Status: MVP demo funcional
Uso: estudo, protótipo e validação visual
Dinheiro real: não
Pix real: não
Payout real: não
```

---

## 📄 Licença

Defina a licença conforme seu objetivo.

Sugestão para projeto privado/comercial:

```txt
All rights reserved.
```

Sugestão para open source:

```txt
MIT License
```

---

## 👤 Autor

Projeto criado como MVP técnico para estudo de:

- Telegram Mini Apps.
- FastAPI.
- Bot com aiogram.
- Painel administrativo.
- Animações com Canvas.
- Fluxos de invoice demo.
- RTP automático.
- Prototipação de produto.

---

## ⚠️ Aviso final

Este projeto é apenas uma demonstração técnica.

Não use para operação real de apostas, jogos de azar, pagamentos ou sorteios com dinheiro real sem orientação jurídica e autorização adequada.
