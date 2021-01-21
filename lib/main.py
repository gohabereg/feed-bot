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

from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
from pymongo import MongoClient
from auth import AuthServer
from urllib.parse import urlencode

from dotenv import load_dotenv, find_dotenv
import asyncio

load_dotenv(find_dotenv())

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)

# Define a few command handlers. These usually take the two arguments update and
# context. Error handlers also receive the raised TelegramError object in error.


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    qs = urlencode({
        'state': update.message.from_user.id,
        'client_id': os.getenv('VK_CLIENT_ID'),
        'redirect_uri': 'http://' + os.getenv('HOST') + ':' + os.getenv('AUTH_PORT') +  '/callback',
        'response_type': 'code',
        'v': 5.126,
        'scope': 'wall'
    })
    url = "https://oauth.vk.com/authorize?"+qs

    keyboard = [
        [InlineKeyboardButton(
            "Авторизоваться в ВК", url=url)],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text('Привет!', reply_markup=reply_markup)


def help_command(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /help is issued."""
    update.message.reply_text('Help!')


def echo(update: Update, context: CallbackContext) -> None:
    """Echo the user message."""
    update.message.reply_text(update.message.text)


def auth_callback(tg_id):
    bot = Bot(os.getenv('TG_BOT_TOKEN'))
    bot.send_message(tg_id, "Вы успешно авторизовались!")


def main():
    # client = MongoClient('db', username='root', password='root')

    # db = client['bot']
    """Start the bot."""
    # Create the Updater and pass it your bot's token.
    # Make sure to set use_context=True to use the new context based callbacks
    # Post version 12 this will no longer be necessary
    updater = Updater(
        os.getenv('TG_BOT_TOKEN'), use_context=True)

    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # on different commands - answer in Telegram
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("help", help_command))

    # on noncommand i.e message - echo the message on Telegram
    dispatcher.add_handler(MessageHandler(
        Filters.text & ~Filters.command, echo))

    # Start the Bot
    updater.start_polling()

    # Run the bot until you press Ctrl-C or the process receives SIGINT,
    # SIGTERM or SIGABRT. This should be used most of the time, since
    # start_polling() is non-blocking and will stop the bot gracefully.
    server = AuthServer(auth_callback)


if __name__ == '__main__':
    main()
