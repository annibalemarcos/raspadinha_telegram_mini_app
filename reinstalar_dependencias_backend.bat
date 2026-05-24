@echo off
cd /d "%~dp0"

echo.
echo Limpando ambiente virtual antigo...
if exist .venv (
    rmdir /s /q .venv
)

echo.
echo Criando novo ambiente virtual...
python -m venv .venv

echo.
echo Ativando ambiente...
call .venv\Scripts\activate

echo.
echo Atualizando pip...
python -m pip install --upgrade pip setuptools wheel

echo.
echo Instalando dependencias travadas...
pip install -r backend\requirements.txt

echo.
echo Rodando seed...
if exist raspadinha.db (
    echo Banco antigo encontrado: raspadinha.db
    echo Se voce mudou estrutura, apague manualmente com: del raspadinha.db
)
python scripts\seed_demo.py

echo.
echo Iniciando backend...
python backend\run.py

pause
