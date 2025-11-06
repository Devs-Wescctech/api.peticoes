import json, os
from fastapi import Request
from .config import settings
from .database import DefaultSessionLocal, make_session_for_url

TENANTS_MAP = None

def load_tenants_map():
    global TENANTS_MAP
    if TENANTS_MAP is not None:
        return TENANTS_MAP
    path = os.path.join(os.path.dirname(__file__), "..", "config", "tenants.json")
    path = os.path.abspath(path)
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            TENANTS_MAP = json.load(f)
    else:
        TENANTS_MAP = {}
    return TENANTS_MAP

def get_session_maker_for_request(request: Request):
    """ Retorna uma Session factory conforme TENANT_MODE.
    - single: usa sessão padrão
    - multi_db: usa X-Tenant para escolher a URL correspondente
    """
    mode = settings.TENANT_MODE.lower().strip()
    if mode != "multi_db":
        return DefaultSessionLocal

    tenants = load_tenants_map()
    tenant_header = settings.TENANT_HEADER
    tenant_key = request.headers.get(tenant_header)
    if tenant_key and tenant_key in tenants:
        return make_session_for_url(tenants[tenant_key])
    # fallback (sem header ou não mapeado)
    return DefaultSessionLocal
