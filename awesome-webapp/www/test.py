import orm
import asyncio
from models import User, Blog, Comment

async def test(loop):
    #change your settins here
    await orm.create_pool(loop=loop, user='www-data', password='www-data', db='awesome')
    u = User(name='Test', email='test@qq.com', passwd='1234567890', image='about:blank')
    await u.save()
    ## 网友指出添加到数据库后需要关闭连接池，否则会报错 RuntimeError: Event loop is closed
    orm.__pool.close()
    await orm.__pool.wait_closed()

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(test(loop))
    loop.close()

#参考资料: https://aodabo.tech/blog/001546713871394a2814d2c180b4e6f8d30c62a3eaf218a000
