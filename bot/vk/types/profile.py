from .sex import Sex
from .online_info import OnlineInfo

class Profile:
    def __init__(self, api_response):
        self.first_name = api_response['first_name']
        self.id = api_response['id']
        self.last_name = api_response['last_name']
        self.can_access_closed = api_response['can_access_closed']
        self.is_closed = api_response['is_closed']
        self.sex = Sex(api_response['sex'])
        self.screen_name = api_response['screen_name']
        self.photo_50 = api_response['photo_50']
        self.photo_100 = api_response['photo_100']
        self.online_info = OnlineInfo(api_response['online_info'])
        self.online = api_response['online']