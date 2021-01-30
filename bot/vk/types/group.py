class Group:
    def __init__(self, api_response):
        self.id = api_response['id']
        self.name = api_response['name']
        self.screen_name = api_response['screen_name']
        self.type = api_response['type']
        self.photo_50 = api_response['photo_50']
        self.photo_100 = api_response['photo_100']
        self.photo_200 = api_response['photo_200']
