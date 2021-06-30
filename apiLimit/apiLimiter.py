import aioredis,uvicorn,time,logging
from fastapi import Depends, FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi_utils.tasks import repeat_every


class Cache:
    def __init__(self):
        """self.s_time = time.time()"""
        self.token = 0

    def checkToken(self):
        """
        # for handled by request
        if time.time() - self.s_time >= 60:
            self.s_time = time.time()
            self.token = 0
        """
        if self.token < 10:
            self.token += 1
            return {'msg':'hello world'} 
        return {'msg':'too many requests received'}

logger = logging.getLogger(__name__)
app = FastAPI()
cache = Cache()

@app.on_event("startup")
@repeat_every(seconds=60,logger=logger,wait_first=True)
def resetToken():
    global cache
    cache.token = 0

@app.get("/")
async def index():
    return cache.checkToken()

# @app.on_event("startup")
# async def startup():
#     redis = await aioredis.create_redis_pool("redis://127.0.0.1:6379")
#     await FastAPILimiter.init(redis)

# @app.get("/", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
# async def index():
#     return {"msg": "Hello World"}
    
    
if __name__ == "__main__":
    """
    learn leaking bucket algorithm
    so far using token bucket algorithm 
    """
    uvicorn.run("apiLimiter:app", debug=True, reload=True)
    
