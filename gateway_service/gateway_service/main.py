from typing import Dict

import uvicorn
from fastapi import FastAPI, status

app = FastAPI()


@app.get('/manage/health', status_code=status.HTTP_200_OK)
async def check_health() -> Dict:
    return {'Service': 'Gateway'}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
