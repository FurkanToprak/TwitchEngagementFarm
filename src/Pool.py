from Bot import Bot
from Channel import Channel
import logging

logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

class Pool:
    def __init__(self, bots: list[Bot]) -> None:
        if (len(bots) == 0):
            logging.error('Cannot have a Pool without bots!')
        self.bots = bots
        self.masterBot = bots[0]
        self.id = self.masterBot.getUsername()
    
    def getId(self) -> str:
        return self.id

    def getBots(self) -> list[Bot]:
        return self.bots

    def joinChannel(self, channel: Channel):
        pass

    def followChannel(self, channel: Channel):
        pass

    def chat(self, messages: list[str]):
        pass

    def chatSpam(self, message: str):
        pass

# TODO: implement in parallel do for each Bot 