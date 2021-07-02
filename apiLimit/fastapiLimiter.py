import aioredis,uvicorn,time,logging
from fastapi import Depends, FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi_utils.tasks import repeat_every

class Cache:
    def __init__(self, limit=10,update=60,rate=6):
        self.s_time = time.time()
        self.token = 0
        self.limit = limit
        self.rate = rate
        self.update = update
        self.bucket = []
        
    def checkToken(self):
        """
        # for handled by request
        if time.time() - self.s_time >= 60:
            self.s_time = time.time()
            self.token = 0
        """
        if self.token < self.limit:
            self.token += 1
            return {'msg':'hello world'} 
        return {'msg':'too many requests received'}       

logger = logging.getLogger(__name__)
app = FastAPI()
cache = Cache()

@app.get("/")
async def index():
    global cache
    print("CACHE INFO: ",len(cache.bucket))
    if len(cache.bucket) < cache.limit:
        cache.bucket.append("hello world")
    if time.time() - cache.s_time >= cache.rate:
        cache.s_time = time.time()
        return {'msg':cache.bucket.pop(0)}
    return {'msg':'too many requests received'}

@app.on_event("startup")
@repeat_every(seconds=cache.update,logger=logger,wait_first=True)
def resetToken():
    global cache
    cache.token = 0
    cache.bucket.clear()

# @app.get("/")
# async def index():
#     return cache.checkToken()

# @app.on_event("startup")
# async def startup():
#     redis = await aioredis.create_redis_pool("redis://127.0.0.1:6379")
#     await FastAPILimiter.init(redis)

# @app.get("/", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
# async def index():
#     return {"msg": "Hello World"}
    
    
if __name__ == "__main__":
    """
    leaking bucket algorithm - standart rate response
    token bucket algorithm - with burst
    """
    uvicorn.run("fastapiLimiter:app", debug=True, reload=True)
    
