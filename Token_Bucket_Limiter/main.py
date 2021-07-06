import aioredis,uvicorn,time,logging
from deta import Deta
from fastapi import Depends, FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from fastapi_utils.tasks import repeat_every

class Cache:
    def __init__(self, limit=10,update=60,rate=6):
        self.s_time = time.time()
        self.update_time = time.time()
        self.token = 0
        self.limit = limit
        self.rate = rate
        self.update = update
        self.bucket = []

        deta = Deta("c0v7erzu_UMHnYtbdHmMAz4A1uzdbKhiZ7nvS2Ds5")
        self.db = deta.Base('Cache')
        self.db.put({'message':'Hello world','key':str(self.token)})

    def checkToken(self):
        
        # for handled by request
        if time.time() - self.update_time >= 60:
            self.update_time = time.time()
            self.token = 0
        if self.token < self.limit:
            self.token += 1
            return {'msg':'hello world'} 
        return {'msg':'too many requests received'}   

    def __str__(self):
        return f"CACHE INFO: {len(self.bucket)}"    

"""
global variable objects
"""
logger = logging.getLogger(__name__)
app = FastAPI(title="api rate limiter")
cache = Cache()
# LOCAL_REDIS_USL = "redis://127.0.0.1:6379"

"""
using detabases
"""
@app.get("/detabase/{message}")
async def index(message:str):
    global cache
    if time.time() - cache.update_time >= 60:
        cache.update_time = time.time()
        cache.token = 0
    if int(cache.db.get(str(cache.token))['key']) < cache.limit:
        cache.token += 1
        cache.db.put({'message':message,'key':str(cache.token)})
    if time.time() - cache.s_time >= cache.rate:
        cache.s_time = time.time()
        return {'msg':cache.db.get(str(cache.token))['message'],'count':cache.db.get(str(cache.token))['key']}
    return {'msg':'too many requests received','count':cache.db.get(str(cache.token))['key']}

"""
Implementation of both token algorithm and leaky bucket.
Object storage base and requests function based
"""
@app.get("/tokenAlgo")
async def index():
    return cache.checkToken()

@app.get("/bucketAlgo/{message}")
async def index(message:str):
    global cache
    # print(cache)
    if len(cache.bucket) < cache.limit:
        cache.bucket.append(message)
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


"""
Uses packaged aioredis integrated with FastAPILimiter
"""
# @app.on_event("startup")
# async def startup():
#     redis = await aioredis.create_redis_pool(LOCAL_REDIS_URL)
#     await FastAPILimiter.init(redis)

# @app.get("/", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
# async def index():
#     return {"msg": "Hello World"}
    
    
if __name__ == "__main__":
    """
    leaking bucket algorithm - standart rate response
    token bucket algorithm - with burst
    """
    uvicorn.run("main:app", debug=True, reload=True)