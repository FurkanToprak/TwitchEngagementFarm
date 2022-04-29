from typing import Union
import requests
import logging
import json
from . import ChannelModel

logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

class Bot:
    def __init__(self, username: str, password: str, email: str, userId: str, token: str) -> None:
        self.username = username
        self.password = password
        self.email = email
        self.userId = userId
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
        self.channel = None
    
    def getUsername(self):
        return self.username
    
    def getPassword(self):
        return self.password

    def getEmail(self):
        return self.email

    def getToken(self):
        return self.token

    def getChannel(self) -> Union[None, ChannelModel.Channel]:
        return self.channel

    def fetchChannelId(self, channelName: str) -> str:
        """ Fetches the ID of a given channel. """
        accessToken = 'qecxhnjevnnfvskhhd07od91yliqti'
        cl= 'https://api.twitch.tv/api/channels/' + channelName + '/access_token?need_https=true&oauth_token=' + accessToken
        logging.debug('Channel post link for _cid created: %s' % cl)   
        print(self.requestHeader)
        channel = requests.get(cl, headers=self.requestHeader)
        logging.debug(channel.text)
        print('fetched channel') #FIXME: 404 error
        print(channel)
        try:
            tokenInfo = channel.json()['token'] 
            channelId = json.loads(tokenInfo)['channel_id']
            logging.info(f'[{self.getUsername()}] Fetched channel ID {channelId} for {channelName}.')
            return channelId    
        except KeyError:
            logging.error(f'[{self.getUsername()}] Could not fetch channel ID for {channelName}.')
            return ''

    def followChannel(self, channel: ChannelModel.Channel) -> bool:
        payload = '[{\"operationName\":\"FollowButton_FollowUser\",\"variables\":{\"input\":{\"disableNotifications\":false,\"targetID\":\"%s\"}},\"extensions\":{\"persistedQuery\":{\"version\":1,\"sha256Hash\":\"51956f0c469f54e60211ea4e6a34b597d45c1c37b9664d4b62096a1ac03be9e6\"}}}]' % channel.getChannelId()
        r = requests.post('https://gql.twitch.tv/gql', data=payload, headers=self.requestHeader)
        if 'error' in r.text:
            logging.error(f'[{self.getUsername()}] [Path 1] Error in following channel {channel.getChannelName()}.')
            logging.error(r.text)
        else:
            try:
                followedChannel = r.json()[0]['data']['followUser']['follow']['user']
                logging.info(f'[{self.getUsername()}] Success following channel {channel.getChannelName()}.')
                logging.debug(followedChannel)
                self.channel = channel
                return True
            except Exception as e:
                logging.error(f'[{self.getUsername()}] [Path 2] Error in following channel {channel.getChannelName()}.')
                logging.error(e)
        return False

    def unfollowChannel(self, channel: ChannelModel.Channel) -> bool:
        payload = '[{"operationName":"FollowButton_UnfollowUser","variables":{"input":{"targetID":"%s"}},"extensions":{"persistedQuery":{"version":1,"sha256Hash":"d7fbdb4e9780dcdc0cc1618ec783309471cd05a59584fc3c56ea1c52bb632d41"}}}]' % channel.getChannelId()
        r = requests.post('https://gql.twitch.tv/gql', data=payload, headers=self.requestHeader)
        if 'error' in r.text:
            logging.error(f'[{self.getUsername()}] [Path 1] Error in unfollowing channel {channel.getChannelName()}.')
            logging.error(r.text)
        else:
            try:
                requestId = r.json()[0]['extensions']['requestID']
                logging.info(f'[{self.getUsername()}] Success following channel {channel.getChannelName()} [RequestID={requestId}].')
                return True
            except Exception as e:
                logging.error(f'[{self.getUsername()}] [Path 2] Error in unfollowing channel {channel.getChannelName()}.')
                logging.error(e)
        return False
    
    def joinChannel(self, channel: ChannelModel.Channel) -> bool:
        pass
    
    def chatChannel(self, channel: ChannelModel.Channel) -> bool:
        pass

# TODO: add chat and join channel options based off of twitch IRC

