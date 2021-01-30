class ProfileInfo:
    def __init__(self, api_response):
        self.first_name = api_response['first_name']
        self.last_name = api_response['last_name']
