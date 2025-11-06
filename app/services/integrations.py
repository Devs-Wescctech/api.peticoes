# Stubs de integrações (SendGrid, WhatsApp, IA, LLM). Preencha com SDKs reais conforme necessidade.
def send_email(to: str, subject: str, html: str, text: str | None = None, sender_email: str | None = None, sender_name: str | None = None):
    return {"status": "queued", "to": to, "subject": subject}

def send_whatsapp(phone: str, message: str, api_token: str | None = None):
    return {"status": "queued", "phone": phone}

def generate_image(prompt: str):
    return {"url": "https://example.com/fake-image.jpg"}

def invoke_llm(prompt: str, response_json_schema: dict | None = None):
    # Apenas ecoa o prompt; implemente provedor real (OpenAI, etc.) caso necessário
    return {"title": "Título (mock)", "description": "Descrição (mock)", "echo": prompt}
