from flask import Flask, Response, request
from services import Services
from renderer import Renderer
import json



app = Flask(__name__)
services = Services()
renderer = Renderer()

@app.route("/ping")
def ping():
    return "Pong!"


@app.route("/")
def Home():
    return GetThreadsDefault()
@app.route("/GETTHREADS")
def GetThreadsDefault():
    return GetThreads(0)
@app.route("/GETTHREADS/<int:firstindex>")
def GetThreads(firstindex):
	gui = bool(request.args.get('gui'))
	result = services.getThreads(firstindex)

	if not gui:
		result = renderer.RenderGUI(contenttype = 'threads', json = json.loads(result))
		header = ''
	else:
		header = 'application/json'


	print result
	return Response(result, mimetype = header)

@app.route("/GETCHAT")
def GetChatDefault():
    return GetChat(0)
@app.route("/GETCHAT/<int:index>")
def GetChat(index):
	gui = bool(request.args.get('gui'))
	moremessages = bool(request.args.get('nummessages'))
	nummessages = int(request.args.get('nummessages')) if moremessages else 20
	print str(moremessages) + " " + str(nummessages)
	result = services.getChat(index, nummessages)

	if gui:
		result = renderer.RenderGUI(contenttype = 'chat', json = json.loads(result))
		header = ''
	else:
		header = 'application/json'

	print result
	return Response(result, mimetype = header)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 4460, debug = True)
