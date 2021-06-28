import aioredis
import uvicorn
from fastapi import Depends, FastAPI

from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter

app = FastAPI()

@app.on_event("startup")
async def startup():
    redis = await aioredis.create_redis_pool("redis://127.0.0.1:6379")
    await FastAPILimiter.init(redis)

@app.get("/", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def index():
    return {"msg": "Hello World"}


if __name__ == "__main__":
    uvicorn.run("main:app", debug=True, reload=True)