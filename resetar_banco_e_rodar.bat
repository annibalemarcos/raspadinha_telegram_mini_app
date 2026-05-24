@echo off
cd /d "%~dp0"
call .venv\Scripts\activate

if exist raspadinha.db (
    del raspadinha.db
)

python scripts\seed_demo.py
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --app-dir backend

pause
