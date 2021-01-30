from .size import Size

class Photo:
    def __init__(self, api_response):
        self.album_id = api_response['album_id']
        self.date = api_response['date']
        self.id = api_response['id']
        self.owner_id = api_response['owner_id']

        if 'access_key' in api_response:
            self.access_key = api_response['access_key']
        else:
            self.access_key = None

        self.sizes = list(map(lambda size: Size(size), api_response['sizes']))
        self.text = api_response['text']

        if 'user_id' in api_response:
            self.user_id = api_response['user_id']
        else:
            self.user_id = None

    @ property
    def url(self):
        return next((x for x in self.sizes if x.type == 'x'), self.sizes[0]).url
