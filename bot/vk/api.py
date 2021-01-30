import vk_api
import os
from .types.newsfeed import NewsFeed
from .types.video import Video
from .types.profile_info import ProfileInfo
from .types.post import Post
from .types.like_result import LikeResult
from .types.repost_result import RepostResult


class VkApi:
    def __init__(self, login, password=None):
        self.session = vk_api.VkApi(login=login, password=password, app_id=os.getenv(
            'VK_CLIENT_ID'), scope='wall,friends,offline')

        self.session.auth(token_only=True)
        self.api = self.session.get_api()

    def get_newsfeed(self, start_time):
        return NewsFeed(self.api.newsfeed.get(filters='post', count=100, start_time=start_time))

    def get_video(self, owner_id, video_id, access_key=''):
        video_id = str(owner_id) + '_' + str(video_id) if access_key == '' else str(
            owner_id) + '_' + str(video_id) + '_' + str(access_key)

        return Video(self.api.video.get(owner_id=owner_id, videos=video_id)['items'][0])

    def get_profile_info(self):
        return ProfileInfo(self.api.account.getProfileInfo())

    def get_post(self, post_id):
        return Post(self.api.wall.getById(posts=post_id)[0])

    def like_add(self, owner_id, item_id, item_type='post'):
        return LikeResult(self.api.likes.add(owner_id=owner_id, item_id=item_id, type=item_type))

    def like_delete(self, owner_id, item_id, item_type='post'):
        return LikeResult(self.api.likes.delete(owner_id=owner_id, item_id=item_id, type=item_type))

    def wall_repost(self, owner_id, post_id):
        return RepostResult(self.api.wall.repost(object='wall{}_{}'.format(owner_id, post_id)))

    def fave_add_post(self, owner_id, post_id):
        return bool(self.api.fave.addPost(owner_id=owner_id, id=post_id))

    def fave_remove_post(self, owner_id, post_id):
        return bool(self.api.fave.removePost(owner_id=owner_id, id=post_id))
