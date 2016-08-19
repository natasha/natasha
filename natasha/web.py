from ujson import dumps
from aiohttp import web
from natasha import Combinator, DEFAULT_GRAMMARS


def serialize(results):
    for (grammar, rule, match) in results:
        yield {
            'grammar': grammar.__name__,
            'rule': rule,
            'match': match,
        }

async def index(request):
    form = await request.post()
    results = app['combinator'].extract(form['text'])
    return web.json_response(list(serialize(results)), dumps=dumps)


app = web.Application()
app['combinator'] = Combinator(DEFAULT_GRAMMARS)
app.router.add_route('POST', '/', index)

if __name__ == "__main__":
    web.run_app(app)
