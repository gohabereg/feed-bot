from .photo import Photo
from .link import Link
from .video import Video
from .doc import Doc

class Attachment:
    def __init__(self, api_reponse):
        self.type = api_reponse['type']

        if self.type == 'photo':
            self.item = Photo(api_reponse['photo'])
        elif self.type == 'link':
            self.item = Link(api_reponse['link'])
        elif self.type == 'video':
            self.item = Video(api_reponse['video'])
        elif self.type == 'doc':
            self.item = Doc(api_reponse['doc'])
        else:
            self.item = None
