from .photo import Photo

class Link:
    def __init__(self, api_response):
        self.url = api_response['url']
        self.title = api_response['title']
        self.caption = api_response['caption']
        self.description = api_response['description']
        self.photo = Photo(api_response['photo'])
        if 'is_favorite' in api_response:
            self.is_favorite = api_response['is_favorite']
        else:
            self.is_favorite = False