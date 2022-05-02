from . import ChannelModel
from python_twitch_irc import TwitchIrc
from time import time
from . import config
from random import randint
import logging


logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)
def getRandomDelay():
    newDelay = randint(config.minDelay, config.maxDelay)
    logging.debug(f'Waiting {newDelay} seconds.')
    return newDelay

# TODO: logging
class IRCBot(TwitchIrc):
    def __init__(self, username: str, token: str, channel: ChannelModel.Channel):
        self.channel = channel
        self.username = username
        self.queue = []
        self.idleUntil = time()
        super().__init__(username, token)

    def queueMessage(self, newMessage: str):
        self.queue.append(newMessage)

    def on_connect(self):
        logging.debug(f'{self.username} connecting to channel {self.channel.getChannelName()}')
        self.join(f'#{self.channel.getChannelName()}')

    def on_message(self, timestamp, tags, channel, user, message):
        logging.debug(f'[{timestamp}] Message from {user} in channel {channel}: {message}')
        if len(self.queue) == 0:
            return
        if time.time() - self.idleUntil < config.minDelay:
            return # log
        # pop off queue
        nextMessage = self.queue.pop(0)
        # chats to channel
        logging.debug(f'[{timestamp}] Sending message to channel {channel} from user {self.username}')
        self.message(channel, nextMessage)
        # reset timer
        self.idleUntil = time() + getRandomDelay()