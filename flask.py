from aiohttp import web
from datetime import datetime
import uuid

ads = {}

routes = web.RouteTableDef()


@routes.post('/ads')
async def create_ad(request):
    data = await request.json()

    required_fields = {'title', 'description', 'owner'}
    if not required_fields.issubset(data):
        raise web.HTTPBadRequest(text='Missing required fields')

    ad_id = str(uuid.uuid4())
    ad = {
        'id': ad_id,
        'title': data['title'],
        'description': data['description'],
        'owner': data['owner'],
        'created_at': datetime.utcnow().isoformat()
    }

    ads[ad_id] = ad
    return web.json_response(ad, status=201)


@routes.get('/ads/{ad_id}')
async def get_ad(request):
    ad_id = request.match_info['ad_id']
    ad = ads.get(ad_id)

    if not ad:
        raise web.HTTPNotFound(text='Ad not found')

    return web.json_response(ad)


@routes.put('/ads/{ad_id}')
async def update_ad(request):
    ad_id = request.match_info['ad_id']
    ad = ads.get(ad_id)

    if not ad:
        raise web.HTTPNotFound(text='Ad not found')

    data = await request.json()

    ad['title'] = data.get('title', ad['title'])
    ad['description'] = data.get('description', ad['description'])
    ad['owner'] = data.get('owner', ad['owner'])

    return web.json_response(ad)


@routes.delete('/ads/{ad_id}')
async def delete_ad(request):
    ad_id = request.match_info['ad_id']

    if ad_id not in ads:
        raise web.HTTPNotFound(text='Ad not found')

    del ads[ad_id]
    return web.json_response({'status': 'deleted'})


app = web.Application()
app.add_routes(routes)

if __name__ == '__main__':
    web.run_app(app)