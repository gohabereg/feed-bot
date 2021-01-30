from .sex import Sex
from .online_info import OnlineInfo


class Profile:
    def __init__(self, api_response):
        self.first_name = api_response['first_name']
        self.id = api_response['id']
        self.last_name = api_response['last_name']
        self.sex = Sex(api_response['sex'])
        self.photo_50 = api_response['photo_50']
        self.photo_100 = api_response['photo_100']
        self.online_info = OnlineInfo(api_response['online_info'])
        self.online = api_response['online']
