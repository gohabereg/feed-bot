class RepostResult:
    def __init__(self, api_reponse):
        self.likes_count = api_reponse['likes_count']
        self.post_id = api_reponse['post_id']
        self.reposts_count = api_reponse['reposts_count']
