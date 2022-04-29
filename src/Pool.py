from math import ceil
from typing import Union
from . import Bot, Channel
import logging

logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

class Pool:
    def __init__(self, bots: list[Bot.Bot]) -> None:
        if (len(bots) == 0):
            logging.error('Cannot have a Pool without bots!')
        self.bots = bots
        self.masterBot = bots[0]
        self.id = self.masterBot.getUsername()
        self.channel = None
    
    def getId(self) -> str:
        return self.id
    
    def getChannel(self) -> Union[Channel.Channel, None]:
        return self.channel

    def getBots(self) -> list[Bot.Bot]:
        return self.bots

    def joinChannel(self, channel: Channel.Channel):
        for bot in self.bots:
            bot.joinChannel(channel)
        logging.info(f'Pool {self.getId()} followed channel {channel.getChannelName()}')

    def followChannel(self, channel: Channel.Channel):
        logging.info(f'Pool {self.getId()} has started to follow channel {channel.getChannelName()}')
        for bot in self.bots:
            bot.followChannel(channel)
        logging.info(f'Pool {self.getId()} followed channel {channel.getChannelName()}')

    def chatChannel(self, messages: list[str]):
        if self.getChannel() is None:
            logging.warning('Need to join a channel before chatting! Aborting.')
            return;
        logging.info(f'Starting chat with {len(messages)} messages in channel {self.getChannel().getChannelName()}')
        if (len(messages) > len(self.getBots())):
            diff = len(self.getBots()) - len(messages)
            maxDiffPerBot = ceil(diff / len(self.getBots)) 
            logging.info(f'More bots than messages. At least one bot will say {maxDiffPerBot} things.')
        elif (len(messages) < len(self.getBots())):
            idleBots = len(self.getBots()) - len(messages)
            logging.info(f'More bots than messages. {idleBots} bots will not say anything.')
        else:
            # of messages matches # of bots in pool.
            for messageIndex, message in messages:
                bot = self.bots[botIndex]
                botIndex = messageIndex % len(self.getBots())
                logging.debug(f'[{messageIndex}] {bot.getUsername()} is chatting [{message}] in channel {self.getChannel().getChannelName()}')
                bot.chatChannel(message)


    def chatSpamChannel(self, message: str):
        if self.getChannel() is None:
            logging.warning('Need to join a channel before chatting! Aborting.')
            return;
        logging.info(f'Starting to spam {message} in channel {self.getChannel().getChannelName()}')
        for bot in self.getBots():
                bot.chatChannel(message)

# TODO: implement in parallel do for each Bot 