import logging
import subprocess
from . import Pool, Bot
import random

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
            botLines = botFile.readlines()
            for botLine in botLines:
                if len(botLine) == 0:
                    continue
                try:
                    username, password, email, userId, token = botLine.split(' ')
                    newBot = Bot.Bot(username, password, email, userId, token)
                    if newBot.getUsername() in self.freeBots:
                        logging.info(f'[{i}] Attempted to parse existing free bot from {botListPath}')
                    elif newBot.getUsername() in self.busyBots:
                        logging.info(f'[{i}] Attempted to parse existing busy bot from {botListPath}')
                    else:
                        self.freeBot[newBot.getUsername()] = newBot
                        logging.debug(f'[{i}] Parsed bot {newBot.getUsername()}.')
                except: 
                    logging.error(f'[{i}] Failed parsing bot from {botListPath}')

    def getBusyBots(self) -> dict:
        return self.busyBots
    
    def getFreeBots(self) -> dict:
        return self.freeBots

    def isPoolActive(self, pool: Pool.Pool) -> bool:
        return pool.getId() in self.pools
    
    def allocatePool(self, numBots: int) -> Pool.Pool:
        botList = []
        for _i in range(numBots):
            fetchedBot = self.allocateBot()
            botList.append(fetchedBot)
        newPool = Pool(botList)
        logging.debug(f'Allocated pool of {numBots} users. Pool master is {newPool.getId()}.')
        self.pools[newPool.getId()] = newPool

    def isBotActive(self, bot: Bot.Bot) -> bool:
            return bot.getUsername() in self.busyBots

    def freePool(self, pool: Pool.Pool):
        for bot in pool.getBots():
            self.freeBot(bot)
        self.pools.pop(pool.getId())
        logging.debug(f'Freed pool {pool.getId()}.')


    def allocateBot(self) -> Bot.Bot:
        randomBotUsername = random.choice(list(self.freeBots))
        freeBot: Bot.Bot = self.freeBots.pop(randomBotUsername)
        logging.debug('freeBot')
        logging.debug(freeBot)
        self.busyBots[freeBot.getUsername()] = freeBot
        return freeBot # TODO: check that it's a bot returned

    def freeBot(self, bot: Bot.Bot):
        try:
            busyBot: Bot.Bot = self.busyBots.pop(bot.getUsername())
            self.freeBots[busyBot.getUsername()] = busyBot # TODO: make sure it works
            logging.debug(f'Freed bot {bot.getUsername()}.')
        except KeyError:
            logging.error(f'Bot {bot.getUsername()} was not busy.')