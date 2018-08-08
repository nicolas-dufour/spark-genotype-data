from flask import Flask,jsonify,request
import json, CherryPy
from SQLQueries.queryNucleotides import dbQuery

app = Flask(__name__)
@app.route('/')
def main():
	return('Hello World')
@app.route('/v1/brapi/nucleotidedataquery',methods=['POST'])
def retrieveNucleotideQuery():
	requestJson=request.get_json()
	dbId=requestJson.dbId
	with open('indexDb.json' as index):
		dbPath=index[dbId]
    nucleotides=requestJson.nucleotidesRetrieve
    plantFilter=requestJson.plantFilter
    nucleotideCondition=requestJson.nucleotideCondition
	data=dbQuery(dbPath,nucleotides,plantFilter,nucleotideCondition)
	jsondata='['
	for i in range(1,len(data)):
		jsondata+='{'
		for j in range(len(data[1])-1):
			jsondata+=data[0][j]+": "+data[i][j]+","
		jsondata+=data[0][-1]+": "+data[i][-1]+"},"
	for j in range(len(data[1])-1):
		jsondata+=data[0][j]+": "+data[-1][j]+","
	jsondata+=data[0][-1]+": "+data[-1][-1]+"}]"
	returnstring='{"metadata":{"datafiles":[],"pagination":{"currentPage":0,"pageSize":x,"totalCount":2,"totalPages":1},"status":[]},"result":{"dataType":"Nucleotide Data","data":'+jsondata+',"DbId":'+dbId+'}}'
	return jsonify(returnstring)

def run_server(app):

    # Enable WSGI access logging via Paste
    app_logged = TransLogger(app)

    # Mount the WSGI callable object (app) on the root directory
    cherrypy.tree.graft(app_logged, '/')

    # Set the configuration of the web server
    cherrypy.config.update({
        'engine.autoreload.on': True,
        'log.screen': True,
        'server.socket_port': 8080,
        'server.socket_host': '0.0.0.0'
    })

    # Start the CherryPy WSGI web server
    cherrypy.engine.start()
    cherrypy.engine.block()


if __name__ == "__main__":
    run_server(app)
