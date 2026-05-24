@echo off
cd /d "%~dp0"
if not exist .venv (
    python -m venv .venv
)
call .venv\Scripts\activate
pip install -r backend\requirements.txt
if not exist .env (
    copy .env.example .env
)
python scripts\seed_demo.py
python backend\run.py
pause
