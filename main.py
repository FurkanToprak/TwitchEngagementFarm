import logging
from src.ChannelModel import Channel
from src import config
from src.BotBankModel import BotBank
import os

logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

if __name__ == '__main__':
    logging.info(f"Creating a pool of {config.numBots} bots.")
    if config.resetTokens:
        os.remove(config.botListPath)
        with open(config.botListPath, "w"):
            pass # delete and create empty file
    botStorage = BotBank(config.numBots, config.botGeneratorPath, config.botListPath, config.generateMoreBots)
    poolOne = botStorage.allocatePool(3)
    poolOneMaster = poolOne.getMasterBot()
    # botOne = botStorage.allocateBot()
    channelOne = Channel('Ninja', poolOneMaster) # or call with a single bot like botOne
    # botOne.followChannel(channelOne)
    poolOne.followChannel(channelOne)
