from typing import Dict

import uvicorn
from fastapi import FastAPI, status
from starlette.middleware.cors import CORSMiddleware

from identity_provider.config import DB_CONFIG
from identity_provider.db.db_config import run_db_migrations
from identity_provider.routers import router

app = FastAPI()
app.include_router(router, tags=['Identity Provider API'])

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_health() -> Dict:
    return {'Service': 'Identity Provider'}


if __name__ == "__main__":
    # run_db_migrations(DB_CONFIG.dict(), 'identity_provider/db/migrations/')
    uvicorn.run(app, host="0.0.0.0", port=8030)
