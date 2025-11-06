from fastapi import APIRouter, UploadFile, File, HTTPException, Response
from app.services.files import save_public_file, save_private_file
import os
from app.core.config import settings

router = APIRouter(prefix="/upload", tags=["Upload de Arquivos"])

@router.post("")
async def upload_public(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(400, "Arquivo obrigatório")
    return save_public_file(file)

@router.post("/private")
async def upload_private(file: UploadFile = File(...)):
    if not file:
        raise HTTPException(400, "Arquivo obrigatório")
    return save_private_file(file)

# Servir arquivos públicos
@router.get("/../files/{filename}")
def serve_public(filename: str):
    path = os.path.join(settings.FILE_STORAGE_DIR, "public", filename)
    if not os.path.exists(path):
        raise HTTPException(404, "Arquivo não encontrado")
    with open(path, "rb") as f:
        content = f.read()
    return Response(content=content, media_type="application/octet-stream")

# Servir arquivo privado com token=filename simples (stub)
@router.get("/../files/private/{token}")
def serve_private(token: str):
    filename = token  # stub
    path = os.path.join(settings.FILE_STORAGE_DIR, "private", filename)
    if not os.path.exists(path):
        raise HTTPException(404, "Arquivo não encontrado")
    with open(path, "rb") as f:
        content = f.read()
    return Response(content=content, media_type="application/octet-stream")
