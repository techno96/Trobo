import time, flask, pickle, json, sys
import pandas as pd
import numpy as np
from googleapiclient import discovery
from flask_cors import CORS, cross_origin

# initialize flask object
app = flask.Flask(__name__)
cors = CORS(app, resources={r"/predict": {"origins": "http://localhost:3000"}})
#initialize API key for perpspective API
API_KEY = 'AIzaSyC4zu-biGJBTDft7HBOFzzqQrrTMa1-JIs'

# compute model predictions using Perpective API
def compute_predictions(test_term, strategy):
    # configuring the client for the Perpspective API
    client = discovery.build(
    'commentanalyzer',
    'v1alpha1',
    developerKey = API_KEY,
    discoveryServiceUrl = 'https://commentanalyzer.googleapis.com/$discovery/rest?version=v1alpha1',
    static_discovery = False,
    )

    # configuring the request
    analyze_request = {
    'comment': { 'text': test_term },
    'requestedAttributes': {'SEVERE_TOXICITY': {}},
    'languages': ['en']
    }
    
    # inititalize response score
    sev_toxicity = 0
    try:
        # retrun the rersponse from the Perspective API
        response = client.comments().analyze(body=analyze_request).execute()
        #print('check')

        # categorize the response labels
        sev_toxicity = response['attributeScores']['SEVERE_TOXICITY']['spanScores'][0]['score']['value']
        #print(str(sev_toxicity))
        
        # return response according to the input strategy
        threshold = 0.5
        if strategy.casefold() == "Toxic".casefold() and sev_toxicity > threshold :
            return sev_toxicity, "TOXIC TOXIC TOXIC!"
            
        elif strategy.casefold() != "Toxic".casefold() and sev_toxicity > threshold:
            df = pd.read_csv('C:/Users/sharv/Desktop/Trobo/Trobo_data.csv')
            indices = df.index[df['STRATEGY'] == strategy]
            return sev_toxicity, df.iloc[np.random.choice(indices)].DATA

        else:
            return sev_toxicity, "NOT TOXIC!"

    except Exception as exception:
        # return an invalid response
        print(exception)
        return sev_toxicity, "No Prediction from Perspective API"

@app.before_request
def before_request():
    flask.g.request_start_time = time.time()
    flask.g.request_time = lambda: (time.time() - flask.g.request_start_time)

# define predict function as an endpoint 
@app.route('/predict', methods = ['GET'])
@cross_origin(origin='*',headers=['access-control-allow-origin','Content-Type'])
# serve predictions
def predict():
   # dict served on api call
    data = {'prediction': [], 'success': False}

    # get request parameters
    params = flask.request.json
    if (params == None):
        params = flask.request.args

    # return classification results if parameters are found
    if (params != None):
        # initialize test term from params
        test_term = params.get('query')

        # initialize strategy from params
        strategy = params.get('strategy')

        # compute model predictions using Perpective API
        score, pred = compute_predictions(test_term, strategy)

        time_1 = flask.g.request_time()
        

        # append predictions & labels to data
        data['prediction'] = pred
        data['success'] = True
        data['score'] = score

    time_2 = flask.g.request_time()
    data['Total_time_taken'] = time_2
        
    # return response in json format 

    response = flask.jsonify(data)
    #response.headers.add('Access-Control-Allow-Origin', '*')

    return response

def main():
    # start the flask app (allow remote connections) 
    app.run(host = '0.0.0.0', port = 9000)    
    
    # exit without errors
    sys.exit(0)
    
if __name__ == '__main__':
    main()
