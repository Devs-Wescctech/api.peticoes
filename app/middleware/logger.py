from fastapi import FastAPI, Request
import time, logging

logger = logging.getLogger("uvicorn.access")

def setup_logger(app: FastAPI):
    @app.middleware("http")
    async def log_requests(request: Request, call_next):
        start = time.time()
        response = await call_next(request)
        elapsed = (time.time() - start) * 1000
        logger.info(f"{request.method} {request.url.path} -> {response.status_code} ({elapsed:.1f} ms)")
        return response
