from .profile import Profile
from .group import Group
from .post import Post

class NewsFeed:
    def __init__(self, api_response):
        self.profiles = list(
            map(lambda profile: Profile(profile), api_response['profiles']))
        self.groups = list(
            map(lambda group: Group(group), api_response['groups']))
        if 'next_from' in api_response:
            self.next_from = api_response['next_from']
        else:
            self.next_from = None
        self.items = list(map(lambda item: Post(
            item, self.groups, self.profiles), api_response['items']))

