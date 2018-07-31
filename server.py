from flask import Flask,jsonify,request

app = Flask(__name__)

@app.route('/v1/brapi/plantgenomequery,' methods=['POST'])
def retrievePlantQuery():
    requestJson=request.get_json()
    sample=
@app.route('/v1/brapi/nucleotidedataquery,' methods=['POST'])
def retrieveNucleotideQuery():
	requestJson=request.get_json()
	dbId=requestJson.dbId
    nucleotides=requestJson.nucleotidesRetrieve
    plantFilter=requestJson.plantFilter
    nucleotideCondition=requestJson.nucleotideCondition

if __name__ == "__main__":
    app.run(debug=True)