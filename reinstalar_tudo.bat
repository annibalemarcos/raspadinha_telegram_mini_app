@echo off
cd /d "%~dp0"
if exist .venv rmdir /s /q .venv
python -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
pip install -r backend\requirements.txt
pip install -r bot\requirements.txt
python -c "import fastapi, aiogram, pydantic; print('OK:', fastapi.__version__, aiogram.__version__, pydantic.__version__)"
pause
