# PetiçõesBR API

API baseada em **FastAPI** para gerenciar petições, assinaturas, campanhas, páginas LinkBio,
templates de mensagem, uploads, integrações, análises, busca e webhooks.

- Linguagem: Python 3.12
- Framework: FastAPI + SQLAlchemy
- Banco: PostgreSQL 16
- Multi-tenant: **multi base** opcional via cabeçalho `X-Tenant` e mapeamento `config/tenants.json`
- Endpoints sob prefixo **/api**

## Estrutura

```
peticoes-api/
├─ app/
│  ├─ main.py
│  ├─ core/
│  │  ├─ config.py
│  │  ├─ database.py
│  │  ├─ security.py
│  │  └─ tenancy.py
│  ├─ middleware/
│  │  ├─ auth.py
│  │  ├─ cors.py
│  │  ├─ errors.py
│  │  └─ logger.py
│  ├─ models/ (SQLAlchemy 2.0)
│  ├─ schemas/ (Pydantic models)
│  ├─ routers/
│  │  ├─ petitions.py
│  │  ├─ signatures.py
│  │  ├─ campaigns.py
│  │  ├─ campaign_logs.py
│  │  ├─ linkbio_pages.py
│  │  ├─ message_templates.py
│  │  ├─ upload.py
│  │  ├─ integrations.py
│  │  ├─ analytics.py
│  │  ├─ search.py
│  │  ├─ webhooks.py
│  │  ├─ users.py
│  │  └─ auth.py
│  ├─ services/
│  │  ├─ files.py
│  │  ├─ csv_export.py
│  │  ├─ analytics.py
│  │  └─ integrations.py
│  ├─ utils/
│  │  ├─ pagination.py
│  │  └─ filters.py
│  ├─ migrations/
│  │  └─ 001_initial_schema.sql
│  └─ config/
│     └─ tenants.json
├─ storage/
│  ├─ public/.keep
│  └─ private/.keep
├─ scripts/
│  └─ apply_migrations.py
├─ Dockerfile
├─ docker-compose.yml
├─ requirements.txt
├─ .env.example
└─ Makefile
```

## Uso rápido (Docker)

1. Copie `.env.example` para `.env` e ajuste variáveis.
2. Suba o stack:
   ```bash
   docker compose up -d --build
   ```
3. Aplique as migrações (roda o SQL bruto fornecido):
   ```bash
   docker compose exec api python scripts/apply_migrations.py
   ```
4. API: http://localhost:3001/docs

## Multi-tenant (multi base)
- Defina `TENANT_MODE=multi_db` no `.env`.
- Edite `app/config/tenants.json` mapeando `"tenant_slug" -> "postgresql+psycopg2://..."`.
- Envie `X-Tenant: tenant_slug` em cada request.
- Sem o header, cai no `DATABASE_URL` padrão (single-tenant).

## Layout de deploy no servidor
- Pensado para o diretório `/peticoes/api`, como você indicou.
- Nginx pode fazer proxy para `api:3001` (container) ou para a porta do host publicada.

---
Gerado em: 2025-11-06T22:48:35.471892Z
