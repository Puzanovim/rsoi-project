from typing import Dict

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from category_service.config import DB_CONFIG
from category_service.db.db_config import run_db_migrations
from category_service.exceptions import NotFoundCategory
from category_service.routers import router

app = FastAPI()
app.include_router(router, tags=['Category API'])


@app.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_health() -> Dict:
    return {'Service': 'Category'}


@app.exception_handler(NotFoundCategory)
async def not_found_category_handler(request: Request, exc: NotFoundCategory) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'message': 'Category not found'},
    )


if __name__ == "__main__":
    run_db_migrations(DB_CONFIG.dict(), 'category_service/db/migrations/')
    uvicorn.run(app, host="0.0.0.0", port=8060)
