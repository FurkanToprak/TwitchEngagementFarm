import logging
import subprocess
from . import BotModel, PoolModel
import random
from typing import Union

logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

class BotBank:
    def __init__(self, numBots: int,  botGeneratorPath: str, botListPath: str, generateMoreBots: bool):
        self.freeBots = {}
        self.busyBots = {}
        self.pools = {}
        if generateMoreBots:
            for i in range(numBots):
                logging.debug(f'[{i}] Running create script for user.')
                output = subprocess.run(f'cd {botGeneratorPath} && echo "" | node index.js', shell=True, capture_output=True)
                # TODO: check that this output ends up in botListPath
                logging.debug(f'[{i}] Completed creation of user.')
        with open(botListPath, 'r') as botFile:
            botLines = botFile.read().split('\n')
            lineIndex = 0
            for botLine in botLines:
                if len(botLine) == 0:
                    break # last line
                try:
                    username, password, email, userId, token = botLine.split(' ')
                    newBot = BotModel.Bot(username, password, email, userId, token)
                    if newBot.getUsername() in self.freeBots:
                        logging.info(f'[{lineIndex}] Attempted to parse existing free bot from {botListPath}')
                    elif newBot.getUsername() in self.busyBots:
                        logging.info(f'[{lineIndex}] Attempted to parse existing busy bot from {botListPath}')
                    else:
                        self.freeBots[newBot.getUsername()] = newBot
                        logging.debug(f'[{lineIndex}] Parsed bot {newBot.getUsername()}.')
                except Exception as e: 
                    logging.error(e)
                    logging.error(f'[{lineIndex}] Failed parsing bot from {botListPath}')
                lineIndex += 1

    def getBusyBots(self) -> dict:
        return self.busyBots
    
    def getFreeBots(self) -> dict:
        return self.freeBots

    def isPoolActive(self, pool: PoolModel.Pool) -> bool:
        return pool.getId() in self.pools
    
    def allocatePool(self, numBots: int) -> Union[None, PoolModel.Pool]:
        if (numBots > len(self.freeBots)):
            logging.error(f'Cannot allocate pool of {numBots} users! The number of free bots is {len(self.getFreeBots())}. The number of busy bots is {len(self.getBusyBots())}.')
            return None
        botList = []
        for _i in range(numBots):
            fetchedBot = self.allocateBot()
            botList.append(fetchedBot)
        newPool = PoolModel.Pool(botList)
        logging.debug(f'Allocated pool of {numBots} users. Pool master is {newPool.getId()}.')
        self.pools[newPool.getId()] = newPool
        return newPool

    def isBotActive(self, bot: BotModel.Bot) -> bool:
            return bot.getUsername() in self.busyBots

    def freePool(self, pool: PoolModel.Pool):
        for bot in pool.getBots():
            self.freeBot(bot)
        self.pools.pop(pool.getId())
        logging.debug(f'Freed pool with master bot {pool.getId()}.')


    def allocateBot(self) -> BotModel.Bot:
        randomBotUsername = random.choice(list(self.freeBots))
        freeBot: BotModel.Bot = self.freeBots.pop(randomBotUsername)
        logging.debug('freeBot')
        logging.debug(freeBot)
        self.busyBots[freeBot.getUsername()] = freeBot
        return freeBot # TODO: check that it's a bot returned

    def freeBot(self, bot: BotModel.Bot):
        try:
            busyBot: BotModel.Bot = self.busyBots.pop(bot.getUsername())
            self.freeBots[busyBot.getUsername()] = busyBot # TODO: make sure it works
            logging.debug(f'Freed bot {bot.getUsername()}.')
        except KeyError:
            logging.error(f'Bot {bot.getUsername()} was not busy.')