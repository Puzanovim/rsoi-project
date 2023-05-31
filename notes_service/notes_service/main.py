from typing import Dict

import uvicorn
from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse

from notes_service.config import DB_CONFIG
from notes_service.db.db_config import run_db_migrations
from notes_service.exceptions import NotFoundNote
from notes_service.routers import router

app = FastAPI()
app.include_router(router, prefix='/notes', tags=['Notes API'])


@app.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_health() -> Dict:
    return {'Service': 'Notes'}


@app.exception_handler(NotFoundNote)
async def not_found_note_handler(request: Request, exc: NotFoundNote) -> JSONResponse:
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={'message': 'Note not found'},
    )


if __name__ == "__main__":
    run_db_migrations(DB_CONFIG.dict(), 'notes_service/db/migrations/')
    uvicorn.run(app, host="0.0.0.0", port=8070)
