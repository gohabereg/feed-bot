from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs, urlencode
import requests
import os
from pymongo import MongoClient


class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        parse_result = urlparse(self.path)
        parameters = parse_qs(parse_result.query)

        print(self.path)

        if parse_result.path == '/auth':
            self.auth(parameters['state'][0])
        elif parse_result.path == '/callback':
            code = parameters['code'][0]
            tg_id = parameters['state'][0]
            token, vk_id = self.get_token(code)
            self.write_token_to_db(tg_id, vk_id, token)

            self.send_response(302)
            self.send_header("Location", "https://t.me/" +
                             os.getenv('TG_BOT_USERNAME'))
            self.end_headers()

        else:
            self.send_response(404)
            self.send_header("Content-Type", "text/html")
            self.end_headers()

    def auth(self, state):
        qs = urlencode({
            'state': state,
            'client_id': os.getenv('VK_CLIENT_ID'),
            'redirect_uri': 'http://localhost:8080/callback',
            'response_type': 'code',
            'v': 5.126,
            'scope': 'wall'
        })

        print(os.getenv('VK_CLIENT_ID'))

        self.send_response(302)
        self.send_header("Location", "https://oauth.vk.com/authorize?"+qs)
        self.end_headers()

    def get_token(self, code):
        qs = urlencode({
            'client_id': os.getenv('VK_CLIENT_ID'),
            'client_secret': os.getenv('VK_CLIENT_SECRET'),
            'redirect_uri': 'http://localhost:8080/callback',
            'code': code,
        })
        r = requests.get('https://oauth.vk.com/access_token?' + qs)
        json = r.json()

        return json['access_token'], json['user_id']

    def write_token_to_db(self, tg_id, vk_id, access_token):
        client = MongoClient('db', username='root', password='root')
        db = client['bot']

        users = db.users

        users.update({'tg_id': tg_id, 'vk_id': vk_id},
                     {'tg_id': tg_id, 'vk_id': vk_id, 'vk_token': access_token}, True)


class AuthServer:
    def __init__(self, host='0.0.0.0', port=8080):
        self.server = HTTPServer(
            (host, port), MyHandler)

    def start(self):
        self.server.serve_forever()

    def stop(self):
        self.server.server_close()
