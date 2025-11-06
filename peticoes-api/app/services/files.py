import os, secrets, shutil
from fastapi import UploadFile
from app.core.config import settings

def save_public_file(file: UploadFile) -> dict:
    fname = secrets.token_hex(12) + "_" + file.filename.replace(" ", "_")
    target = os.path.join(settings.FILE_STORAGE_DIR, "public", fname)
    with open(target, "wb") as f:
        shutil.copyfileobj(file.file, f)
    url = f"{settings.BASE_URL}/api/files/{fname}"
    return {"file_url": url, "filename": fname}

def save_private_file(file: UploadFile) -> dict:
    fname = secrets.token_hex(12) + "_" + file.filename.replace(" ", "_")
    target = os.path.join(settings.FILE_STORAGE_DIR, "private", fname)
    with open(target, "wb") as f:
        shutil.copyfileobj(file.file, f)
    # token simples (não persistente): apenas retorna o path-claim (em produção, ideal assinar com expiração)
    token = fname  # placeholder
    url = f"{settings.BASE_URL}/api/files/private/{token}"
    return {"file_url": url, "filename": fname}
