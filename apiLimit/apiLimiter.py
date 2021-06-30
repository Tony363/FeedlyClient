import aioredis,uvicorn,time
from fastapi import Depends, FastAPI
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from multiprocessing import Process,Value,Manager


class Cache:
    def __init__(self):
        self.s_time = time.time()
        self.token = 0
        self.manager = Manager()
        self.mul_token = self.manager.Value('i',0)

    def checkToken(self):
        print(time.time() - self.s_time)
        if time.time() - self.s_time >= 60:
            self.s_time = time.time()
            self.token = 0
        if self.token < 10:
            self.token += 1
            return {'msg':'hello world'} 
        return {'msg':'too many requests received'}

    def checkCalls(self):
        if self.mul_token.value >= 10:
            return {'msg':'too many requests received'}
        self.mul_token.value += 1
        return {'msg':'hello world'}

    def updateToken(self):
        print(time.time() - self.s_time >= 60)
        if time.time() - self.s_time >= 60:
            self.s_time = time.time()
            self.mul_token.value = 0


app = FastAPI()
cache = Cache()

@app.get('/')
async def index():
    return cache.checkCalls()

# @app.get("/")
# async def index():
#     return cache.checkToken()

# @app.on_event("startup")
# async def startup():
    # redis = await aioredis.create_redis_pool("redis://127.0.0.1:6379")
    # await FastAPILimiter.init(redis)

# @app.get("/", dependencies=[Depends(RateLimiter(times=2, seconds=5))])
# async def index():
#     return {"msg": "Hello World"}@app.get("/")
    
    
if __name__ == "__main__":
    p1 = Process(target=uvicorn.run("apiLimiter:app", debug=True, reload=True))
    p1.start()
    p2 = Process(target=cache.updateToken)
    p2.start()
    
    p1.join()
    p2.join()
    
