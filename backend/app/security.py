import hashlib
import hmac
import secrets
from fastapi import Request, HTTPException
from starlette.responses import RedirectResponse

PBKDF2_PREFIX = "pbkdf2_sha256"
ITERATIONS = 260000

def hash_password(password: str) -> str:
    salt = secrets.token_hex(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        salt.encode("utf-8"),
        ITERATIONS
    ).hex()
    return f"{PBKDF2_PREFIX}${ITERATIONS}${salt}${digest}"

def verify_password(password: str, password_hash: str) -> bool:
    if not password_hash:
        return False

    # Novo formato nativo, sem passlib/bcrypt.
    if password_hash.startswith(PBKDF2_PREFIX + "$"):
        try:
            _, iterations, salt, digest = password_hash.split("$", 3)
            candidate = hashlib.pbkdf2_hmac(
                "sha256",
                password.encode("utf-8"),
                salt.encode("utf-8"),
                int(iterations)
            ).hex()
            return hmac.compare_digest(candidate, digest)
        except Exception:
            return False

    # Fallback simples para ambientes antigos/dev.
    # Se o banco antigo tinha hash bcrypt/passlib, apague raspadinha.db e rode seed novamente.
    return False

def require_admin(request: Request):
    if not request.session.get("admin"):
        raise HTTPException(status_code=401, detail="Não autenticado")
    return request.session.get("admin")

def redirect_if_not_admin(request: Request):
    if not request.session.get("admin"):
        return RedirectResponse("/admin/login", status_code=303)
    return None
