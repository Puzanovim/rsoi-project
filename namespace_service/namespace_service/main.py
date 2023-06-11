from typing import Dict

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from namespace_service.config import DB_CONFIG
from namespace_service.db.db_config import run_db_migrations
from namespace_service.exceptions import NotFoundNamespace
from namespace_service.routers import router

app = FastAPI()
app.include_router(router, prefix='/namespaces', tags=['Namespace API'])


@app.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_health() -> Dict:
    return {'Service': 'Namespace'}


@app.exception_handler(NotFoundNamespace)
async def not_found_namespace_handler(request: Request, exc: NotFoundNamespace) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'message': 'Namespace not found'},
    )


if __name__ == "__main__":
    run_db_migrations(DB_CONFIG.dict(), 'namespace_service/db/migrations/')
    uvicorn.run(app, host="0.0.0.0", port=8050)
