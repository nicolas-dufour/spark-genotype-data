from flask import Flask,request,jsonify
import json, cherrypy
from SQLQueries.queryNucleotides import dbQuery
from paste.translogger import TransLogger

app = Flask(__name__)
@app.route('/')
def main():
	return('Hello World')
@app.route('/v1/brapi/nucleotidedataquery',methods=['POST'])
def retrieveNucleotideQuery():
	requestJson=request.get_json()
	dbId=requestJson['dbId']
	with open('indexDb.json') as index:
		index=json.load(index)
		dbPath=index[str(dbId)]
	nucleotides=requestJson['nucleotidesRetrieve']
	plantFilter=requestJson['plantFilter']
	nucleotideCondition=requestJson['nucleotideCondition']
	data=map(lambda x:json.loads(x),dbQuery(dbPath,nucleotides,plantFilter,nucleotideCondition))
	returnjson={"metadata":{"datafiles":[],"pagination":{"currentPage":0,"pageSize":1,"totalCount":2,"totalPages":1},"status":[]},"result":{"dataType":"Nucleotide Data","data":data,"DbId":dbId}}
	return (jsonify(returnjson))

def run_server(app):

	# Enable WSGI access logging via Paste
	app_logged = TransLogger(app)

	# Mount the WSGI callable object (app) on the root directory
	cherrypy.tree.graft(app_logged, '/')

	# Set the configuration of the web server
	cherrypy.config.update({
		'engine.autoreload.on': True,
		'log.screen': True,
		'server.socket_port': 5432,
		'server.socket_host': '0.0.0.0'
	})

	# Start the CherryPy WSGI web server
	cherrypy.engine.start()
	cherrypy.engine.block()


if __name__ == "__main__":
	run_server(app)
