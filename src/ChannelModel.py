class Channel:
    """ Abstraction of a Twitch Channel. """
    def __init__(self, channelName: str, masterBot) -> None:
        self.channelName = channelName
        self.channelId = masterBot.fetchChannelId(channelName)

    def getChannelName(self):
        return self.channelName

    def getChannelId(self):
        return self.channelId