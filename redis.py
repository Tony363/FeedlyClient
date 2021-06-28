import asyncio
import aioredis

async def go():
    redis = await aioredis.create_redis_pool(
        'redis://localhost')
    await redis.set('my-key', 'value')
    val = await redis.get('my-key', encoding='utf-8')
    print(val)
    redis.close()
    await redis.wait_closed()

asyncio.run(go())
# will print 'value'