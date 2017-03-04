from fbparser import FBParser
import json

class Services():
	def __init__(self):
		pass

	def getThreads(self, firstthreadindex):
		response = {}

		fbparser = FBParser(debug = False)
		threads = fbparser.getThreadsSummary(start = firstthreadindex, end = firstthreadindex + 20)

		response["info"] = {
			"numthreads": len(threads),
			"firstthreadindex": firstthreadindex }
		response["threads"] = {}
		for i in range(0, len(threads)):
			lastmessage = ("You : " if threads[i][1][0][1] == fbparser.client_uid else "") + threads[i][1][0][2]
			response["threads"][i] = {
				"threadid":        threads[i][0][0],
				"type":            threads[i][0][1],
				"convoname":       threads[i][0][2],
				"time":            threads[i][0][3],
				"lastmessagebody": lastmessage   }


		data = json.dumps(response, indent = 4, sort_keys = True)
		return data

	def getChat(self, messageindex, nummessages = 20):
		print "Getting chat with {} messages".format(nummessages)
		response = {}

		fb_parser = FBParser(debug = True)
		messages = fb_parser.getThreadMessages(messageindex, messageend = nummessages)[0]

		response["info"] = {
			"nummessages": len(messages[1]),
			"chatindex": messageindex
		}

		response["thread"] = {
			"header": {
				"threadid":  messages[0][0],
				"type":      messages[0][1],
				"convoname": messages[0][2],
				"time":      messages[0][3],
				"participants": {}
			}
		}
		for i in range(0, len(messages[0][4])):
			response["thread"]["header"]["participants"][i] = {
				"uid":  messages[0][4][i][0],
				"name": messages[0][4][i][1],
				"type": messages[0][4][i][2]
			}

		response["thread"]["messages"] = {}
		for i in range(0, len(messages[1])):
			response["thread"]["messages"][i] = {}
			response["thread"]["messages"][i]["body"] = messages[1][i][2]
			response["thread"]["messages"][i]["authorid"] = messages[1][i][1]

			for j in range(0, len(messages[0][4])):
				print str(messages[1][i][1]) + " " + str(messages[0][4][j][0])
				if messages[1][i][1] == messages[0][4][j][0]: #search for the participant with this ID
					response["thread"]["messages"][i]["name"] = messages[0][4][j][1]
					response["thread"]["messages"][i]["type"] = messages[0][4][j][2]
		data = json.dumps(response, indent = 4, sort_keys = True)
		return data