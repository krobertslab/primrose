'''
  Author: Sam Shenoi 
  Description: This file contains the main functionality for the REST API. The rest API sends data to the frontend website
  Date Created: 6/3/2019
'''

#Import Dependencies
from flask import Flask
from flask import jsonify
from Elastic import Elastic
from flask_cors import CORS

#Start up the flask app
app = Flask(__name__)
CORS(app)
ElasticClient = Elastic(abQuery=0,tQuery=5)
#Start up the elastic connection 

import json
#from MachineLearning import Predict
#from MachineLearning import DeepPredict


#Define some routes so that data can be sent
@app.route('/')
def hello_world():
    return "Hello World"

'''
  name    - serach abstracts
  parameters 
          - Disease      - the cancer disease we are looking for. Must be a string 
          - Gene         - the gene that we are interested in 
          - Demographic  - The demographic that the person is a part of 
  return 
          - returns a json object with the top 10 results 
'''
@app.route('/search/abstracts/<string:disease>/<string:gene>/<string:dem>')
def abSearch(disease, gene, dem):
    
        res = ElasticClient.abstractSearch(disease, gene, dem, "")
        f = open("absFile.txt","w")
        f.write(json.dumps(res))
        f.close()
        return jsonify(res)


'''
  name    - serach clinical trials
  parameters 
          - Disease      - the cancer disease we are looking for. Must be a string 
          - Gene         - the gene that we are interested in 
          - Demographic  - The demographic that the person is a part of 
  return 
          - returns a json object with the top 10 results 
'''
@app.route('/search/trials/<string:disease>/<string:gene>/<string:dem>')
def clinSearch(disease, gene, dem):
    res = ElasticClient.trialsSearch(disease, gene, dem,"")
    f = open("trialsFile.txt","w")
    f.write(json.dumps(res))
    f.close()
    return jsonify(res)