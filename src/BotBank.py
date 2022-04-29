import logging
import subprocess
from Pool import Pool
from Bot import Bot
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
                # TODO: scrape results from the botListPath and also validate output with logging
                # TODO: add bot to busy bots
                logging.debug(f'[{i}] Completed creation of user.')
        with open(botListPath, 'r') as botFile:
            botLines = botFile.readlines()
            for botLine in botLines:
                if len(botLine) == 0:
                    continue
                username, password, email, userId, token = botLine.split(' ')
                newBot = Bot(username, password, email, userId, token)

    def isPoolActive(self, pool: Pool) -> bool:
        return pool.getId() in self.pools
    
    def allocatePool(self, numBots: int) -> Pool:
        newPool = Pool([])
        self.pools[newPool.getId()] = newPool

    def freePool(self, pool: Pool):
        for bot in pool.getBots():
            self.freeBot(bot)
        self.pools.pop(pool.getId())

    def allocateBot(self) -> Bot:
        pass

    def freeBot(self, bot: Bot):
        try:
            self.busyBots.pop(bot.getUsername())
            logging.debug(f'Freed bot {bot.getUsername()}.')
        except KeyError:
            logging.error(f'Bot {bot.getUsername()} was not busy.')

    def documentInvalidBots(bots: list[Bot]):
        pass
