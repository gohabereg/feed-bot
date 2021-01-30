from .attachment import Attachment
from .likes import Likes
from .reposts import Reposts


class Post:
    def __init__(self, api_response, groups=[], profiles=[]):
        self.groups = groups
        self.profiles = profiles
        self.source_id = api_response['source_id'] if 'source_id' in api_response else api_response['owner_id']
        self.date = api_response['date']
        self.text = api_response['text']

        if 'copy_history' in api_response:
            self.copy_history = list(map(lambda post: Post(
                post, groups, profiles), api_response['copy_history']))
        else:
            self.copy_history = []

        if 'marked_as_ads' in api_response:
            self.marked_as_ads = api_response['marked_as_ads']
        else:
            self.marked_as_ads = False

        if 'attachments' in api_response:
            self.attachments = list(map(lambda attachment: Attachment(
                attachment), api_response['attachments']))
        else:
            self.attachments = []

        if 'likes' in api_response:
            self.likes = Likes(api_response['likes'])
        else:
            self.likes = Likes(
                {'count': 0, 'user_likes': 0, 'can_like': 0, 'can_publish': 0})
        self.is_favorite = bool(
            api_response['is_favorite']) if 'is_favorite' in api_response else False
        self.post_id = api_response['post_id'] if 'post_id' in api_response else api_response['id']
        self.reposts = Reposts(api_response['reposts']) if 'reposts' is api_response else Reposts(
            {'count': 0, 'user_reposted': 0})

    @ property
    def url(self):
        return 'https://vk.com/wall' + str(self.source_id) + '_' + str(self.post_id)

    @ property
    def author(self):
        if self.source_id < 0:
            return next(
                (x for x in self.groups if x.id == abs(self.source_id)), None).name
        else:
            profile = next(
                (x for x in self.profiles if x.id == abs(self.source_id)), None)

            return "{} {}".format(profile.first_name, profile.last_name)

    @ property
    def full_text(self):
        text = ''

        if len(self.links):
            urls = list(map(lambda x: x.item.url, self.links))

            text += '<a href="{}">&#8203;</a>'.format('\n'.join(urls))

        text += '<a href="{}">{}</a>\n\n{}'.format(
            self.url, self.author, self.text)

        return text

    @ property
    def links(self):
        return list(filter(lambda x: x.type == 'link', self.attachments))

    @ property
    def photos(self):
        return list(filter(lambda x: x.type == 'photo', self.attachments))

    @ property
    def videos(self):
        return list(filter(lambda x: x.type == 'video', self.attachments))

    @property
    def docs(self):
        return list(filter(lambda x: x.type == 'doc', self.attachments))
