@echo off
cd /d "%~dp0"

if not exist .venv (
    python -m venv .venv
)

call .venv\Scripts\activate

python -m pip install --upgrade pip setuptools wheel
pip install -r bot\requirements.txt

python bot\bot.py

pause
