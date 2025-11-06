from fastapi import APIRouter

router = APIRouter(prefix="/webhooks", tags=["Webhooks"])

@router.post("")
def create_webhook(payload: dict):
    # Stub: persistir em tabela webhooks, se necessário
    return {"ok": True, "id": "mock"}

@router.get("")
def list_webhooks():
    return []

@router.delete("/{id}")
def delete_webhook(id: str):
    return {"ok": True}
