# Correção: conflito entre aiogram e pydantic

Erro visto:

```txt
ResolutionImpossible
ModuleNotFoundError: No module named 'aiogram'
```

O `aiogram` não foi instalado porque houve conflito com a versão fixada do `pydantic`.

## Correção aplicada

As dependências foram ajustadas para:

```txt
pydantic==2.9.2
pydantic-core==2.23.4
aiogram==3.15.0
```

Essas versões ficam melhor casadas para este MVP.

## Como corrigir no Windows

Rode:

```bat
reinstalar_tudo.bat
```

Ou manualmente:

```powershell
rmdir /s /q .venv
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
pip install -r backend\requirements.txt
pip install -r bot\requirements.txt
python -c "import fastapi, pydantic, pydantic_core, aiogram; print('OK')"
```
