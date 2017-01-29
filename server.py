from flask import Flask, Response
from services import Services



app = Flask(__name__)
services = Services()

@app.route("/ping")
def ping():
    return "Pong!"


@app.route("/GETTHREADS")
def GetThreadsDefault():
    return GetThreads(0)
@app.route("/GETTHREADS/<int:firstindex>")
def GetThreads(firstindex):
	result = services.getThreads(firstindex)
	print result
	return Response(result, mimetype='application/json')

@app.route("/GETCHAT/<int:index>")
def GetChat(index):
	result = services.getChat(index)
	print result
	return Response(result, mimetype='application/json')

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = 4460, debug = True)
