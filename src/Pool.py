from Bot import Bot
from Channel import Channel

class Pool:
    def __init__(self, bots: list[Bot]) -> None:
        self.bots = bots
    
    def getBots(self) -> list[Bot]:
        pass

    def joinChannel(self, channel: Channel):
        pass

    def followChannel(self, channel: Channel):
        pass

    def chat(self, messages: list[str]):
        pass

    def chatSpam(self, message: str):
        pass