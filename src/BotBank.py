import logging
import subprocess
from Pool import Pool
from Bot import Bot
logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

class BotBank:
    def __init__(self, numBots: int,  botGeneratorPath: str, tokenListPath: str, generateMoreBots: bool):
        if generateMoreBots:
            for i in range(numBots):
                logging.debug(f'[{i}] Running create script for user.')
                output = subprocess.run(f'cd {botGeneratorPath} && echo "" | node index.js', shell=True)
                logging.debug(f'[{i}] Completed creation of user.')

    
    def allocatePool(numBots: int) -> Pool:
        pass

    def freePool(pool: Pool):
        pass

    def allocateUser() -> Bot:
        pass

    def freeUser(user: Bot):
        pass
