class Reposts:
    def __init__(self, api_response):
        self.count = api_response['count']
        self.user_reposted = api_response['user_reposted']
