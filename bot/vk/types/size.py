class Size:
    def __init__(self, api_response):
        self.type = api_response['type']
        self.url = api_response['url']
        self.height = api_response['height']
        self.width = api_response['width']