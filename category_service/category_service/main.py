from typing import Dict

import uvicorn
from fastapi import FastAPI, status

from category_service.config import DB_CONFIG
from category_service.db.db_config import run_db_migrations

app = FastAPI()


@app.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_health() -> Dict:
    return {'Hello': 'World'}


if __name__ == "__main__":
    run_db_migrations(DB_CONFIG.dict(), 'category_service/db/migrations/')
    uvicorn.run(app, host="0.0.0.0", port=8060)
