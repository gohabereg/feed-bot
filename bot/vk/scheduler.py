from pymongo import MongoClient
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from threading import Timer
import os
import time
from .api import VkApi
from vk_api.exceptions import ApiError
from ..helpers import create_reply_markup


class Scheduler:
    def __init__(self):
        self.db = MongoClient(os.getenv('MONGO_URL'))['bot']
        self.bot = Bot(os.getenv('TG_BOT_TOKEN'))
        self.running = False
        self.error_sent = {}

    def run(self):
        if self.running:
            return

        self._timer = Timer(10.0, self.send_news_for_all_users)
        self._timer.start()
        self.running = True

    def stop(self):
        if self._timer:
            self._timer.cancel()

        self.running = False
        self._timer = None

    def get_users(self):
        return self.db.users.find({})

    def update_start_time(self, tg_id, login):
        self.db.users.update_one({'tg_id': tg_id, 'login': login}, {
                                 '$set': {'start_time': int(time.time())}})

    def send_news_for_all_users(self):
        users = self.get_users()

        for user in users:
            print(user)
            tg_id = user['tg_id']
            login = user['login']
            start_time = user['start_time']

            try:
                self.update_start_time(tg_id, login)

                self.send_news(tg_id, login, start_time)
                print('news sent')
            # except Exception as e:
            #     print(e)
            except ApiError as e:
                if (tg_id in self.error_sent):
                    pass

                if (str(e).startswith('[5] User authorization failed')):
                    self.bot.send_message(
                        tg_id, 'Срок действия токена истек, пожалуйста авторизуйтесь еще раз с помощью команды /login')
                else:
                    self.bot.send_message(
                        tg_id, 'Произошла ошибка при обращении к API ВКонтакте')

                self.error_sent[tg_id] = True

        self.running = False
        self.run()

    def send_news(self, tg_id, login, start_time):
        vk = VkApi(login)

        news = vk.get_newsfeed(start_time)

        for post in news.items:
            text = post.full_text
            media = []

            if len(post.videos):
                for video in post.videos:
                    if video.player:
                        text += "\n\n{}".format(video.player)
                    else:
                        text += "\n\n{}".format(vk.get_video(video.owner_ud,
                                                             video.id, video.access_key).player)

            if len(post.photos):
                media = list(map(lambda attachments: InputMediaPhoto(
                    attachments.item.url, parse_mode='HTML'), post.photos))

            markup = create_reply_markup(
                post.likes, post.reposts, post.is_favorite, post.source_id, post.post_id)

            if len(media) > 0:
                self.bot.send_media_group(
                    tg_id, media=media)

            self.bot.send_message(
                tg_id, text, parse_mode='HTML', reply_markup=markup, disable_web_page_preview=len(media) > 0)
