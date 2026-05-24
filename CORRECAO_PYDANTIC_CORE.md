# Correção: ImportError pydantic_core

Erro:

```txt
ImportError: cannot import name 'validate_core_schema' from 'pydantic_core'
```

Isso acontece quando `pydantic` e `pydantic-core` ficam em versões incompatíveis dentro do `.venv`.

## Correção aplicada

As dependências foram travadas:

```txt
pydantic==2.10.4
pydantic-core==2.27.2
```

Também foi adicionado:

```txt
reinstalar_dependencias_backend.bat
```

## Como resolver no Windows

Rode:

```bat
reinstalar_dependencias_backend.bat
```

Ou manualmente:

```powershell
rmdir /s /q .venv
python -m venv .venv
.venv\Scripts\activate
python -m pip install --upgrade pip setuptools wheel
pip install -r backend\requirements.txt
python scripts\seed_demo.py
python backend\run.py
```
