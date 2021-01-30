class Likes:
    def __init__(self, api_response):
        self.count = api_response['count']
        self.user_likes = bool(api_response['user_likes'])
        self.can_like = bool(api_response['can_like'])
        self.can_publish = bool(api_response['can_publish'])
