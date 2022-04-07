import redis

from aiohttp import web

KEY = 'merge'


async def convert(request):
    """
    POST
    """
    try:
        from_ = request.query.get('from')
        to_ = request.query.get('to')
        amount_ = request.query.get('amount')
        return web.json_response({
            'status': 'OK',
            'message': _convert(int(amount_), to_, from_)
        })
    except Exception as ex:
        return web.json_response({
            'status': 'FAILED',
            'message': str(ex)
        })


async def redis_abc(request):
    """
    GET
    """
    try:
        value = request.query.get('merge')
        redis_client = redis.Redis(host='localhost', port=6379, db=0)
        redis_client.set(KEY, value)
        redis_client.close()
        return web.json_response({
            'status': 'OK',
            'message': f'merge_status: {value}'
        })
    except Exception as ex:
        return web.json_response({
            'status': 'FAILED',
            'message': str(ex)
        })


def _convert(summ, to_, from_):
    """
    Конвертация валюты
    """
    curr = {
        'USD': 1,
        'RUR': 30
    }
    heft = summ / curr[to_]
    return round(heft * curr[from_], 2)


if __name__ == '__main__':
    app = web.Application()
    app.router.add_post('/database', redis_abc)
    app.router.add_get('/convert', convert)

    web.run_app(app)

    redis_client = redis.Redis(host='localhost', port=6379, db=0)
    # дефолтное значение
    redis_abc(KEY, 0)

    redis_client.close()
