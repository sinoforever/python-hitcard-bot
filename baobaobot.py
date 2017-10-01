#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Simple Bot to reply to Telegram messages. This is built on the API wrapper, see
# echobot2.py to see the same example built on the telegram.ext bot framework.
# This program is dedicated to the public domain under the CC0 license.
import logging
import telegram
from telegram.error import NetworkError, Unauthorized
from time import sleep
from datetime import datetime


update_id = None
user_seen = []

def main():
    global update_id
    global user_seen
    # Telegram Bot Authorization Token
    bot = telegram.Bot('471298728:AAEaSsvHx321R9Q7mrc1aoQCyxViwBnzcmY')

    # get the first pending update_id, this is so we can skip over it in case
    # we get an "Unauthorized" exception.
    try:
        update_id = bot.get_updates()[0].update_id
    except IndexError:
        update_id = None

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    while True:
        try:
            receive_message(bot)
        except NetworkError:
            sleep(1)
        except Unauthorized:
            # The user has removed or blocked the bot.
            update_id += 1


def receive_message(bot):
    global update_id
    global user_seen
    # Request updates after the last update_id
    for update in bot.get_updates(offset=update_id, timeout=10):
        update_id = update.update_id + 1

        if update.message:  # your bot can receive updates without messages
            # Reply to the message
            message_text = update.message.text
            if update.message.from_user in user_seen:
                update.message.reply_text("I've seen you before.")
            else:
                update.message.reply_text("First time seeing you, hi!")
                user_seen.append(update.message.from_user)
            if "time" in message_text:
                update.message.reply_text(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            else:
                update.message.reply_text("I don't understand what you are saying.")


if __name__ == '__main__':
    main()
