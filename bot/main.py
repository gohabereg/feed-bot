#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# pylint: disable=W0613, C0116
# type: ignore[union-attr]
# This program is dedicated to the public domain under the CC0 license.

"""
Simple Bot to reply to Telegram messages.
First, a few handler functions are defined. Then, those functions are passed to
the Dispatcher and registered at their respective places.
Then, the bot is started and runs until we press Ctrl-C on the command line.
Usage:
Basic Echobot example, repeats messages.
Press Ctrl-C on the command line or send a signal to the process to stop the
bot.
"""

import logging
import os
import time

from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext, CallbackQueryHandler
from pymongo import MongoClient
from urllib.parse import urlencode
from .vk.api import VkApi
from .vk.scheduler import Scheduler
from .helpers import create_reply_markup
from vk_api.exceptions import BadPassword, TwoFactorError, SecurityCheck, Captcha

from dotenv import load_dotenv, find_dotenv
import asyncio

load_dotenv(find_dotenv('.env.my'))

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


class Bot:
    def __init__(self):
        self.updater = Updater(os.getenv('TG_BOT_TOKEN'), use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.dispatcher.add_handler(
            CommandHandler('start', self.start_command))
        self.dispatcher.add_handler(
            CommandHandler('captcha', self.captcha_command))
        self.dispatcher.add_handler(CommandHandler('help', self.help_command))
        self.dispatcher.add_handler(
            CommandHandler('login', self.login_command))
        self.dispatcher.add_handler(CallbackQueryHandler(self.callback_query))

        self.db = MongoClient(os.getenv('MONGO_URL'))['bot']
        self.scheduler = Scheduler()
        self.captcha = {}

    def run(self):
        self.updater.start_polling()
        self.scheduler.run()
        self.updater.idle()

        pass

    def start_command(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text(
            'Привет!\nЧтобы авторизоваться, используй команду <code>/login login password</code>.\nЕсли у вас включено подтверждение входа, отключите его, чтобы использовать бота.\n\nP.S. Ваш пароль используется только один раз для авторизации и не сохраняется в базе.', parse_mode='HTML')

    def help_command(self, update: Update, context: CallbackContext) -> None:
        update.message.reply_text(
            'Этот бот будет будет присылать вам новости с вашей ленты в ВК (с небольшой задержкой).\n\nВы можете лайкнуть, репостнуть или добавить запись в избранное, используя кнопки под постами.')

    def login_command(self, update: Update, context: CallbackContext) -> None:
        entities = update.message.text.split(' ')

        if (len(entities) < 3):
            update.message.reply_text(
                'Пожалуйста введите команду в формате <code>/login login password</code>', parse_mode="HTML")
            return

        cmd, login, password = entities
        start_time = int(time.time())

        try:
            vk = VkApi(login, password)
            info = vk.get_profile_info()

            self.db.users.update_one({'tg_id': update.message.from_user.id, 'login': login}, {'$set': {
                'tg_id': update.message.from_user.id, 'login': login, 'start_time': start_time}}, upsert=True)

            update.message.reply_text(
                'Вы авторизовались как {} {}'.format(info.first_name, info.last_name))

            scheduler = Scheduler()

            scheduler.send_news(update.message.from_user.id,
                                login, start_time - 10 * 60)
        except BadPassword as e:
            update.message.reply_text('Введен неверный пароль')
        except TwoFactorError as e:
            update.message.reply_text(
                'Чтобы пользоваться ботом, отключите подтвеждение входа в настройках ВКонтакте')
        except SecurityCheck as e:
            update.message.reply_text(
                'Пожалуйста, воспользуйтесь телефоном в качестве логина')
        except Captcha as e:
            update.message.reply_photo(
                e.get_url(), caption='Пожалуйста, введите код с картинки командой /captcha <code>')
            context.user_data['captcha'] = e
        except Exception as e:
            print(e)
            update.message.reply_text('Произошла ошибка, попобуйте снова')

    def captcha_command(self, update: Update, context: CallbackContext) -> None:
        captcha = context.user_data['captcha']
        cmd, code = update.message.text.split(' ')

        captcha.try_again(code)

    def callback_query(self, update: Update, context: CallbackContext) -> None:
        user = self.db.users.find_one(
            {'tg_id': update.callback_query.message.chat.id})

        vk = VkApi(user['login'])

        query = update.callback_query
        command, post_id = query.data.split(' ')
        post = vk.get_post(post_id)
        owner_id, post_id = post_id.split('_')

        likes = post.likes
        reposts = post.reposts
        is_favorite = post.is_favorite

        if command == 'like':
            if post.likes.user_likes:
                result = vk.like_delete(owner_id, post_id)
                likes.count = result.likes
                likes.user_likes = False
                query.answer('Вы убрали лайк с поста')
            else:
                result = vk.like_add(owner_id, post_id)
                likes.count = result.likes
                likes.user_likes = True
                query.answer('Вы лайкнули пост')
        elif command == 'repost':
            if post.reposts.user_reposted:
                query.answer('Вы уже репостнули эту запись')
            else:
                result = vk.wall_repost(owner_id, post_id)
                likes.count = result.likes_count
                reposts.count = result.reposts_count
                reposts.user_reposted = True
                query.answer('Вы репостнули запись')
        elif command == 'fave':
            if post.is_favorite:
                is_favorite = not vk.fave_remove_post(owner_id, post_id)
                if not is_favorite:
                    query.answer('Вы удалили пост из избанного')
                else:
                    query.answer('Произошла ошибка')
            else:
                is_favorite = vk.fave_add_post(owner_id, post_id)
                if is_favorite:
                    query.answer('Вы добвили пост в избранное')
                else:
                    query.answer('Произошла ошибка')

        markup = create_reply_markup(
            likes, reposts, is_favorite, owner_id, post_id)

        update.callback_query.edit_message_reply_markup(
            reply_markup=markup
        )


if __name__ == '__main__':
    bot = Bot()
    bot.run()
