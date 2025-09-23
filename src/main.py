from fastapi import FastAPI
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from src.api.hotels import router as hotel_router
import uvicorn
from src.config import settings

app = FastAPI()
app.include_router(hotel_router)


@app.get('/')
async def status():
    return {"status": "Alive"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
