from fastapi import FastAPI
from app.middleware.cors import setup_cors
from app.middleware.errors import setup_errors
from app.middleware.logger import setup_logger

from app.routers import petitions, signatures, campaigns, campaign_logs, linkbio_pages
from app.routers import message_templates, upload, integrations, analytics, search, webhooks, users, auth

app = FastAPI(title="PeticoesBR API", version="1.0.0", openapi_url="/openapi.json")

setup_cors(app)
setup_errors(app)
setup_logger(app)

api_prefix = "/api"
app.include_router(auth.router, prefix=api_prefix)
app.include_router(users.router, prefix=api_prefix)
app.include_router(petitions.router, prefix=api_prefix)
app.include_router(signatures.router, prefix=api_prefix)
app.include_router(campaigns.router, prefix=api_prefix)
app.include_router(campaign_logs.router, prefix=api_prefix)
app.include_router(linkbio_pages.router, prefix=api_prefix)
app.include_router(message_templates.router, prefix=api_prefix)
app.include_router(upload.router, prefix=api_prefix)
app.include_router(integrations.router, prefix=api_prefix)
app.include_router(analytics.router, prefix=api_prefix)
app.include_router(search.router, prefix=api_prefix)
app.include_router(webhooks.router, prefix=api_prefix)
