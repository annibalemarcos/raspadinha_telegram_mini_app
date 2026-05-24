import os
import asyncio
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, F
from aiogram.types import Message, WebAppInfo
from aiogram.filters import CommandStart
from aiogram.utils.keyboard import InlineKeyboardBuilder

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
MINI_APP_URL = os.getenv("MINI_APP_URL", "http://127.0.0.1:8000/app")

if not TOKEN:
    raise RuntimeError("Defina TELEGRAM_BOT_TOKEN no arquivo .env")

bot = Bot(token=TOKEN)
dp = Dispatcher()

def is_https_url(url: str) -> bool:
    return (url or "").lower().startswith("https://")

def main_menu():
    kb = InlineKeyboardBuilder()

    if is_https_url(MINI_APP_URL):
        kb.button(text="🎟 Abrir Mini App", web_app=WebAppInfo(url=MINI_APP_URL))
        kb.button(text="🌐 Abrir no navegador", url=MINI_APP_URL)
    else:
        # Telegram não aceita WebApp com http://127.0.0.1.
        # Em modo local, mostramos um botão de URL simples e uma mensagem explicando.
        kb.button(text="🌐 Testar local no navegador", url=MINI_APP_URL)

    kb.adjust(1)
    return kb.as_markup()

def https_warning() -> str:
    if is_https_url(MINI_APP_URL):
        return ""

    return (
        "\n\n⚠️ Atenção: o MINI_APP_URL atual é local/http:\n"
        f"{MINI_APP_URL}\n\n"
        "O Telegram só aceita Mini App com URL pública HTTPS.\n"
        "Para testar no Telegram, use ngrok ou Cloudflare Tunnel e coloque a URL https:// no .env."
    )

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer(
        "🎟️ Raspadinha Mini App Demo\n\n"
        "Agora o jogo roda numa tela visual dentro do Telegram:\n"
        "1. Escolha a raspadinha\n"
        "2. Simule o Pix\n"
        "3. Confirme sua chave Pix\n"
        "4. Raspe a tela com animação\n"
        "5. Veja o resultado\n\n"
        "Tudo fictício: Pix fake, payout fake, alegria quase real."
        + https_warning(),
        reply_markup=main_menu()
    )

@dp.message(F.text)
async def fallback(message: Message):
    await message.answer(
        "Abra o Mini App pelo botão abaixo:" + https_warning(),
        reply_markup=main_menu()
    )

async def main():
    print("🤖 Bot rodando com Telegram Mini App...")
    print(f"Mini App URL: {MINI_APP_URL}")
    if not is_https_url(MINI_APP_URL):
        print("⚠️ MINI_APP_URL não é HTTPS. Telegram WebApp exige HTTPS público.")
        print("   Localhost funciona no navegador, mas não como Mini App real.")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
