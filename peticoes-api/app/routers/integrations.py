from fastapi import APIRouter
from app.services.integrations import send_email, send_whatsapp, generate_image, invoke_llm

router = APIRouter(prefix="/integrations", tags=["Integrações"])

@router.post("/send-email")
def integration_email(payload: dict):
    return send_email(payload.get("to"), payload.get("subject"), payload.get("html"),
                      payload.get("text"), payload.get("from"), payload.get("from_name"))

@router.post("/send-whatsapp")
def integration_whatsapp(payload: dict):
    return send_whatsapp(payload.get("phone"), payload.get("message"), payload.get("api_token"))

@router.post("/generate-image")
def integration_generate_image(payload: dict):
    return generate_image(payload.get("prompt"))

@router.post("/invoke-llm")
def integration_invoke_llm(payload: dict):
    return invoke_llm(payload.get("prompt"), payload.get("response_json_schema"))
