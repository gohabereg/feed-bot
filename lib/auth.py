from urllib.parse import urlparse, parse_qs, urlencode
import os
from pymongo import MongoClient
from aiohttp import web, ClientSession


class AuthServer:
    def __init__(self, callback, host='0.0.0.0', port=8080):
        self.auth_callback = callback
        self.app = web.Application()
        self.app.add_routes([
            web.get('/auth', self.handle_auth),
            web.get('/callback', self.handle_callback)
        ])
        self.db = MongoClient('db', username='root', password='root')['bot']

        web.run_app(self.app)

    def handle_auth(self, request):
        qs = urlencode({
            'state': request.query.get('state'),
            'client_id': os.getenv('VK_CLIENT_ID'),
            'redirect_uri': 'http://' + os.getenv('HOST') + ':' + os.getenv('PORT') + '/callback',
            'response_type': 'code',
            'v': 5.126,
            'scope': 'wall'
        })

        raise web.HTTPFound(location="https://oauth.vk.com/authorize?"+qs)

    async def handle_callback(self, request):
        code = request.query.get('code')
        tg_id = request.query.get('state')

        access_token, vk_id = await self.get_token(code)

        self.db.users.update({'tg_id': tg_id, 'vk_id': vk_id},
                             {'tg_id': tg_id, 'vk_id': vk_id, 'vk_token': access_token}, True)

        self.auth_callback(tg_id)

        raise web.HTTPFound(location="https://t.me/" +
                            os.getenv('TG_BOT_USERNAME'))

    async def get_token(self, code):
        params = {
            'client_id': os.getenv('VK_CLIENT_ID'),
            'client_secret': os.getenv('VK_CLIENT_SECRET'),
            'redirect_uri': 'http://' + os.getenv('HOST') + ':' + os.getenv('PORT') + '/callback',
            'code': code,
        }

        async with ClientSession() as session:
            async with session.get('https://oauth.vk.com/access_token', params=params) as response:
                json = await response.json()

                return json['access_token'], json['user_id']
