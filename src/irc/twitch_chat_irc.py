import logging
import socket, re, emoji

class CallbackFunction(Exception):
	"""Raised when the callback function does not have (only) one required positional argument"""
	pass

logging.basicConfig(format='[%(asctime)s] %(message)s', datefmt='%H:%M:%S', level=logging.DEBUG)

class TwitchChatIRC():
	__HOST = 'irc.chat.twitch.tv'
	__PORT = 6667

	__PATTERN = re.compile(r'@(.+?(?=\s+:)).*PRIVMSG[^:]*:([^\r\n]*)')

	__CURRENT_CHANNEL = None

	def __init__(self, username: str, password: str):
		self.__NICK = username
		self.__PASS = password

		# overwrite if specified
		if(username is not None):
			self.__NICK = username
		if(password is not None):
			self.__PASS = 'oauth:'+str(password).lstrip('oauth:')
		
		# create new socket
		self.__SOCKET = socket.socket()
		
		# start connection
		self.__SOCKET.connect((self.__HOST, self.__PORT))
		logging.debug('Connected to',self.__HOST,'on port',self.__PORT)

		# log in
		self.__send_raw('CAP REQ :twitch.tv/tags')
		self.__send_raw('PASS ' + self.__PASS)
		self.__send_raw('NICK ' + self.__NICK)
	
	def __send_raw(self, string):
		self.__SOCKET.send((string+'\r\n').encode('utf-8'))

	def __print_message(self, message):
		logging.debug('['+message['tmi-sent-ts']+']',message['display-name']+':',emoji.demojize(message['message']).encode('utf-8').decode('utf-8','ignore'))

	def __recvall(self, buffer_size):
		data = b''
		while True:
			part = self.__SOCKET.recv(buffer_size)
			data += part
			if len(part) < buffer_size:
				break
		return data.decode('utf-8')#,'ignore'

	def __join_channel(self,channel_name):
		channel_lower = channel_name.lower()

		if(self.__CURRENT_CHANNEL != channel_lower):
			self.__send_raw('JOIN #{}'.format(channel_lower))
			self.__CURRENT_CHANNEL = channel_lower

	def close_connection(self):
		self.__SOCKET.close()
		logging.info('Connection closed')

	def listen(self, channel_name, messages = [], timeout=None, message_timeout=1.0, on_message = None, buffer_size = 4096, message_limit = None, output=None):
		self.__join_channel(channel_name)
		self.__SOCKET.settimeout(message_timeout)

		if(on_message is None):
			on_message = self.__print_message
		
		logging.info('Begin retrieving messages:')

		time_since_last_message = 0
		readbuffer = ''
		try:
			while True:
				try:
					new_info = self.__recvall(buffer_size)
					readbuffer += new_info
					
					if('PING :tmi.twitch.tv' in readbuffer):
						self.__send_raw('PONG :tmi.twitch.tv')

					matches = list(self.__PATTERN.finditer(readbuffer))

					if(matches):
						time_since_last_message = 0

						if(len(matches) > 1):
							matches = matches[:-1] # assume last one is incomplete

						last_index = matches[-1].span()[1]
						readbuffer = readbuffer[last_index:]

						for match in matches:
							data = {}
							for item in match.group(1).split(';'):
								keys = item.split('=',1)
								data[keys[0]]=keys[1]
							data['message'] = match.group(2)

							messages.append(data)

							if(callable(on_message)):
								try:
									on_message(data)
								except TypeError:
									raise Exception('Incorrect number of parameters for function '+on_message.__name__)
							
							if(message_limit is not None and len(messages) >= message_limit):
								return messages
							
				except socket.timeout:
					if(timeout != None):
						time_since_last_message += message_timeout
					
						if(time_since_last_message >= timeout):
							logging.debug('No data received in',timeout,'seconds. Timing out.')
							break
		
		except KeyboardInterrupt:
			logging.info('Interrupted by user.')
			
		except Exception as e:
			logging.error('Unknown Error:',e)
			raise e		
		
		return messages

	def send(self, channel_name, message):
		self.__join_channel(channel_name)
		self.__send_raw('PRIVMSG #{} :{}'.format(channel_name.lower(),message))
		logging.info('Sent "{}" to {}'.format(message,channel_name))
