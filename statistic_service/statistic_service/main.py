from typing import Dict

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from statistic_service.config import DB_CONFIG
from statistic_service.db.db_config import run_db_migrations
from statistic_service.exceptions import NotFoundStatistic
from statistic_service.routers import router

app = FastAPI()
app.include_router(router, prefix='/statistics', tags=['Statistics API'])


@app.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_health() -> Dict:
    return {'Service': 'Statistic'}


@app.exception_handler(NotFoundStatistic)
async def not_found_statistic_handler(request: Request, exc: NotFoundStatistic) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'message': 'Statistic not found'},
    )


if __name__ == "__main__":
    run_db_migrations(DB_CONFIG.dict(), 'statistic_service/db/migrations/')
    uvicorn.run(app, host="0.0.0.0", port=8040)
