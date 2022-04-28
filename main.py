import logging
from src import config
from src.BotBank import BotBank

if __name__ == '__main__':
    print(f"Creating a pool of {config.numBots} bots.")
    botStorage = BotBank.BotBank(config.numBots, config.botGeneratorPath)
