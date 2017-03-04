from datetime import datetime

class Renderer():
	def __init__(self):
		pass

	def RenderGUI(self, contenttype, json):
		#rendering pages
		if   contenttype == 'threads':
			# Rendering header
			result =  """<html>
							<head>
								<meta charset = "UTF-8">
								<style>
									.header {
										background-color: #008AFF;
										padding: 5px;
									}
									.thread {
										background-color: #87C1FF;
										border-radius: 10px;
										margin: 5px;
										margin-left: 3%;
										padding-left: 4px;
									}
									a {
										color: black;
										text-decoration: none;
									}
									.warning {
										color: red;
									}
								</style>
							</head>
							<body>
								<div class = "header">
									<h1>Facebook Messenger</h1>
									<h2>Pierre Laclau</h2>
									<p>Last refreshed : """ + datetime.now().strftime('%d/%m, %H:%M') + """</p>
								</div>"""

			# Rendering messages
			threads = json["threads"]
			for i in range(0, len(threads)):
				result += """
					<a href="/GETCHAT/""" + str(i) + """?gui=true">
					<div class = "thread """ + threads[str(i)]["type"] + """">
						<h4>""" + threads[str(i)]["convoname"] + """</h4>
						<p>""" + threads[str(i)]["lastmessagebody"] + """</p>
					</div>
					</a>
				"""

			result += """	</body>
					</html>"""









		elif contenttype == 'chat':
			# Rendering header
			result =  """	<html>
							<head>
								<meta charset = "UTF-8"/>
								<style>
									.header {
										background-color: #008AFF;
										padding: 5px;
									}
									.message.participant{
										margin-right: 20%;
										margin-left: 3%;
									}
									.message.client {
										background-color: #E5E5EA;
										margin-left: 20%
									}
									.message {
										border-radius: 10px;
										margin: 5px;
										padding-left: 4px;
									}
									"""

			colors = ["#309DFF", "#00A650", "#FF8900", "#B424DF", "#91D013", "#F62222","#FF69A3","#8737F8","#FFD200","#784834","#8D92A8"]
			participants = json["thread"]["header"]["participants"]
			for i in range(0, len(participants)):
				if participants[str(i)]["type"] == "participant":
					p_uid = participants[str(i)]["uid"]
					result += """
									.participant""" + p_uid + """ {
										background-color: """ + colors[i] + """;
									}"""
			result += """
								</style>
							</head>
							<body>
								<div class="send">
									<form action="/SENDMESSAGE/">
										<button name = "submit" value = ></button>
									</form>
								</div>




								<div class = "header">
									<h1>""" + json["thread"]["header"]["convoname"] + """</h1>
									<p>Chat number """ + str(json["info"]["chatindex"]) + """</p>
								</div>"""
			# Rendering messages
			messages = json["thread"]["messages"]
			for i in range(0, len(messages)):
				p_type = "participant " + messages[str(i)]["type"] + messages[str(i)]["authorid"] if messages[str(i)]["type"] == "participant" else messages[str(i)]["type"]
				result += """
					<div class = "message """ + p_type + """">
						<h4>""" + messages[str(i)]["name"] + """</h4>
						<p>""" + messages[str(i)]["body"].replace("\n", "</p><p>") + """</p>
					</div>
				"""
			see_more_messages_link = "/GETCHAT/" + str(json["info"]["chatindex"]) + "?gui=true&nummessages=" + str(int(json["info"]["nummessages"]) + 40)
			result += """
					<a href=" """ + see_more_messages_link + """ ">See more...</a>
				</body>
			</html>"""
		return result

"""
Bubble colors :
	#F62222
	#FF69A3
	#B424DF
	#8737F8
	#309DFF
	#00A650
	#91D013
	#FFD200
	#FF8900
	#784834
	#8D92A8
"""