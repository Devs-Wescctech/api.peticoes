from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import traceback

def setup_errors(app: FastAPI):
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        # Log simplificado; em prod, use logger dedicado
        trace = traceback.format_exc(limit=1)
        return JSONResponse(
            status_code=500,
            content={"detail": "Internal Server Error", "error": str(exc), "trace": trace},
        )
