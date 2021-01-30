class OnlineInfo:
    def __init__(self, api_response):
        self.visible = api_response['visible']
        #self.is_online = api_response['is_online']
        self.is_mobile = api_response['is_mobile']
