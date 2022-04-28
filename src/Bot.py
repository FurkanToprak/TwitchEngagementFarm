import requests
import logging
import json

logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

class Bot:
    def __init__(self, username: str, password: str, email: str, token: str) -> None:
        self.username = username
        self.password = password
        self.email = email
        self.token = token
        self.requestHeader = {
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
            "x-apple-os-version": "12.3.1",
            "Authorization": f"OAuth {token}"
        }
    
    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password

    def getEmail(self):
        return self.email

    def getToken(self):
        return self.token

    def fetchChannelId(self, channelName: str) -> str:
        """ Fetches the ID of a given channel. """
        cl= f'https://api.twitch.tv/api/channels/{channelName}/access_token?need_https=true&oauth_token={self.getToken()}'
        logging.debug('Channel post link for _cid created: %s' % cl)   
        channel = requests.get(cl, headers=self.HEADERS)
        logging.debug(channel.text)
        try:
            tokenInfo = channel.json()['token'] 
            channelId = json.loads(tokenInfo)['channel_id']
            logging.info(f'[{self.getUsername()}] Fetched channel ID {channelId} for {channelName}.')
            return channelId    
        except KeyError:
            logging.error(f'[{self.getUsername()}] Could not fetch channel ID for {channelName}.')
            return ''