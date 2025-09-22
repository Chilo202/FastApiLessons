from fastapi import FastAPI, Response, status
from hotels import router as hotel_router
import uvicorn

app = FastAPI()
app.include_router(hotel_router)


@app.get('/')
async def status():
    return {"status": "Alive"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)
