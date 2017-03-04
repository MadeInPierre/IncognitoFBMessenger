#NEW VERSION
import fbchat

class FBData():
	client = None
	ready = False
	needed_reconnect = False

	@staticmethod
	def connect():
		needed_reconnect = False
		
		if FBData.ready == False:
			print("Connecting to facebook...")
#			FBData.client = fbchat.Client("jackdaxterpl@gmail.com", "MadeInJack")
			FBData.client = fbchat.Client("pielaclau@gmail.com", "1outazimut")
			FBData.ready = True

			needed_reconnect = False
		else:
			print "Facebook connection is on."


class FBParser():
	def __init__(self, debug = False):
		FBData.connect() # make sure facebook is connected
		self.debug = debug
		self.client = FBData.client
		self.client_uid = "100000386870459"#self.client.uid #100014698446620 Jack, 100000386870459 Pierre Laclau
		self.client_name = self.client.getUserInfo(self.client_uid)['name']

		# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
		#                                                       #
		#                    SENDING MESSAGES                   #
		#                                                       #
		# # # # # # # # # # # # # # # # # # # # # # # # # # # # #	
	def sendMessage(self, chat_index):
		threads = self.getThreads(False, (0, chat_index))


	def _getThreadsRaw(self, end = 20):
		threads = self.client.getThreadList(0, end = end)
		threads = list(reversed(sorted(result, key=lambda x: x[0][3])))
		return threads





		# # # # # # # # # # # # # # # # # # # # # # # # # # # # #
		#                                                       #
		#               GETTING THREADS AND CONVOS              #
		#                                                       #
		# # # # # # # # # # # # # # # # # # # # # # # # # # # # #

	def getThreadsSummary(self, start = 0, end = 20):
		return self.getThreads(True, (start, end), (0, 0))

	def getThreadMessages(self, threadindex, messagestart = 0, messageend = 20):
		return self.getThreads(True, (threadindex, threadindex), (messagestart, messageend))

	def getThreads(self, getmessages, threadsrange = (0, 20), messagesrange = (0, 20)):
		result = []
		threads = self.client.getThreadList(0, end = threadsrange[1])
		i = 0
		for thread in threads:
			if i >= threadsrange[0] and i <= threadsrange[1]: 
				thread_index = threadsrange[0] + i

				header = self._getThreadHeader(thread)
				thread_id, thread_type, thread_name, thread_time, thread_participants = header

				if getmessages:
					messages = self._getThreadMessages(header, messagesrange = messagesrange)
					result.append((header, messages))
				else:
					result.append(header)
			i += 1

		result = list(reversed(sorted(result, key=lambda x: x[0][3])))
		return result






	def _getThreadHeader(self, thread):
		'''
		Gives a thread's name, id, type (user or group), timestamp
		argument thread : a thread object coming from fbchat
		'''
		thread_name = thread.name
		thread_type = 'user' if thread_name is u'' else 'group'

		thread_id = None
		thread_participants = []
		for participant in thread.participants:
			p_uid = participant[5:]
			p_type = 'client' if p_uid == self.client_uid else 'participant'
			p_name = self.client.getUserInfo(p_uid)['name'] if p_type == 'participant' else self.client_name
			thread_participants.append((p_uid, p_name, p_type))
			
			if (p_type == 'participant' and thread_type == 'user'):
				thread_id = p_uid
				thread_name = p_name
		if thread_type == 'group':
			thread_id = thread.thread_id

		return (thread_id, thread_type, thread_name, thread.timestamp, thread_participants)



	def _getThreadMessages(self, header, messagesrange = (0, 5)):
		print "Getting messages from " + str(messagesrange[0]) + " to " + str(messagesrange[1])
		result = []
		try:
			messages = self.client.getThreadInfo(userID      = header[0], 
												 start       = messagesrange[0], 
												 end         = messagesrange[1],
												 thread_type = header[1])
			i = 0
			for message in messages:
				if i >= messagesrange[0] and i <= messagesrange[1]:
					message_index = messagesrange[0] + i
					try:
						message_body = messages[i].body
						if message_body == '':
							message_body = 'Photo'
					except: # messages like 'The group name was changed to xx'
						message_body = 'Special message'

					sender_uid = messages[i].author[5:]

					result.append((message_index, sender_uid, message_body))
				i += 1

			return result
		except: # could not fetch the messages for whatever reason
			return [(0, 'error', 'Error')]
