from ctypes import Union
import requests
import logging

logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%H:%M:%S', level=logging.INFO) #change to logging.DEBUG

payloadHeaderTemplate = {
            "content-type": "application/json",
            "accept" : "application/json",
            "api-consumer-type":  "mobile; iOS/203500927335335108",
            "accept-charset": "utf-8",
            "client-id":  "85lcqzxpb9bqu9z6ga1ol55du",
            "accept-language": "en-us",
            "accept-encoding": "br, gzip, deflate",
            "user-agent": "Twitch 203500927335335108 (iPhone; iOS 12.3.1; en_US)",
            "x-apple-model":  "iPhone 7",
            "x-app-version":  "9.10.1",
            "x-apple-os-version": "12.3.1"
}

def parseInput(inputFilePath):
    with open(inputFilePath, 'r') as inputCsv:
        inputCsvLines = inputCsv.read().split('\n')[1:]
        for inputCsvLine in inputCsvLines:
            username, password, _authToken, channels = inputCsvLine.split(',')
            authToken = loginAndGetToken(username, password)
            print('Access Token', authToken)

def loginAndGetToken(username: str, password: str) -> str:
    data = {
        'username': username,
        'password': password,
        'client_id': '85lcqzxpb9bqu9z6ga1ol55du'
        }
    r = requests.post('https://passport.twitch.tv/login', json=data)
    logging.debug(r.text)
    if 'access_token' in r.text:
            token = r.json()['access_token']
            logging.debug(f'Login succeded for {username}. Token:{token}')
            return token
    if 'captcha' in r.text:
        logging.warning(f'Captcha required for {username}.')
    logging.debug('Failed login. Debug: {r.text}')
    return '' 

def createPayloadHeader(authToken):
    payloadHeader = payloadHeaderTemplate
    payloadHeader['Authorization'] = 'OAuth ' + authToken

parseInput('farm.csv')