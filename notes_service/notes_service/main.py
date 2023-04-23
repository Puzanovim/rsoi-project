from typing import Dict

import uvicorn
from fastapi import FastAPI, status

from notes_service.config import DB_CONFIG
from notes_service.db.db_config import run_db_migrations

app = FastAPI()


@app.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_health() -> Dict:
    return {'Service': 'Notes'}


if __name__ == "__main__":
    run_db_migrations(DB_CONFIG.dict(), 'notes_service/db/migrations/')
    uvicorn.run(app, host="0.0.0.0", port=8070)
