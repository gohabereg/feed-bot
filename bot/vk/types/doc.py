from .doc_type import DocType


class Doc:
    def __init__(self, api_response):
        self.id = api_response['id']
        self.owner_id = api_response['owner_id']
        self.title = api_response['title']
        self.size = api_response['size']
        self.ext = api_response['ext']
        self.url = api_response['url']
        self.date = api_response['date']
        self.type = DocType(api_response['type'])
