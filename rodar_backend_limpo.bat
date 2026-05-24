@echo off
cd /d "%~dp0"

if not exist .venv (
    python -m venv .venv
)

call .venv\Scripts\activate

python -m pip install --upgrade pip setuptools wheel
pip install -r backend\requirements.txt

if exist raspadinha.db (
    echo.
    echo ATENCAO: banco antigo encontrado.
    echo Se o login continuar com erro, rode:
    echo del raspadinha.db
    echo python scripts\seed_demo.py
    echo.
)

python scripts\seed_demo.py

echo.
echo Abrindo backend sem reload para erro aparecer mais limpo...
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --app-dir backend

pause
