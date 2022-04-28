import logging
from src import config
from src.BotBank import BotBank
import os

logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

if __name__ == '__main__':
    logging.info(f"Creating a pool of {config.numBots} bots.")
    if config.resetTokens:
        os.remove(config.tokenListPath)
        with open(config.tokenListPath, "w"):
            pass # delete and create empty file
    botStorage = BotBank(config.numBots, config.botGeneratorPath, config.tokenListPath, config.generateMoreBots)
