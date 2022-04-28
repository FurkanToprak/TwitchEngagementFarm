import logging


class BotBank:
    def __init__(self, numBots: int,  botGeneratorPath: str):
        bots = dict()
        with open(inputFilePath, 'r') as inputFile:
            inputLines: list[str] = inputFile.readlines()
            for inputLine in inputLines:
                if ',' not in inputLine:
                    
                    break
                username, token = inputLine.split(',')