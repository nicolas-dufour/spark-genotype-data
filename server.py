from flask import Flask,request,jsonify
import json, cherrypy
from SQLQueries.queryNucleotides import dbQuery as queryMarker
from SQLQueries.queryPlants import dbQuery as querySample
from paste.translogger import TransLogger

app = Flask(__name__)
@app.route('/')
def main():
	return('This is the page for the API to query the parquet files')
@app.route('/v1/brapi/allelematrices-search',methods=['POST'])
def retrieveNucleotideQuery():
	requestJson=request.get_json()
	queryType=requestJson['queryType']
	dbId=requestJson['dbId']
	with open('./indexDb.json') as f:
		index=json.load(f)
		dbPath=index[dbId]
	nucleotides=requestJson['nucleotidesRetrieve']
	plantFilter=requestJson['plantFilter']
	nucleotideCondition=requestJson['nucleotideCondition']
	if(queryType=='M'):
		data=map(lambda x:json.loads(x),queryMarker(dbPath,nucleotides,plantFilter,nucleotideCondition))
		returnjson={"metadata":{"datafiles":[],"pagination":{"currentPage":0,"pageSize":1,"totalCount":2,"totalPages":1},"status":[]},"result":{"dataType":"Marker Data","data":data,"DbId":dbId}}

	elif(queryType=='S'):
		data=map(lambda x:json.loads(x),querySample(dbPath,plantFilter,nucleotides,nucleotideCondition))
		returnjson={"metadata":{"datafiles":[],"pagination":{"currentPage":0,"pageSize":1,"totalCount":2,"totalPages":1},"status":[]},"result":{"dataType":"Sample Data","data":data,"DbId":dbId}}
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
