import time, flask, pickle, json, sys
import pandas as pd
import numpy as np
from googleapiclient import discovery

# initialize flask object
app = flask.Flask(__name__)

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
    'requestedAttributes': {'SEVERE_TOXICITY': {}}
    }
   
    try:
        # retrun the rersponse from the Perspective API
        response = client.comments().analyze(body=analyze_request).execute()

        print('check')

        # categorize the response labels
        sev_toxicity = response['attributeScores']['SEVERE_TOXICITY']['spanScores'][0]['score']['value']


        if strategy == "Toxic" and sev_toxicity > 0.5 :
            return "TOXIC TOXIC TOXIC"
        elif strategy == "Toxic":
            return "NOT_TOXIC"
        else:
            df = pd.read_csv('/Users/erress/Desktop/Personal/GRE/IDP/Shared/Univ_California_SanDiego/WI22/Anti Social Computing/TroBo/Trobo/Trobo_data.csv')
            print('check2')
            print(strategy)
            indices = df.index[df['STRATEGY'] == strategy]
            print(indices)
            return df.iloc[np.random.choice(indices)].DATA


    except Exception as exception:
        # return an invalid response
        return "No Prediction from Perspective API"

@app.before_request
def before_request():
    flask.g.request_start_time = time.time()
    flask.g.request_time = lambda: (time.time() - flask.g.request_start_time)

# define predict function as an endpoint 
@app.route('/predict', methods = ['GET'])
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
        pred = compute_predictions(test_term, strategy)

        time_1 = flask.g.request_time()
        

        # append predictions & labels to data
        data['prediction'] = pred
        data['success'] = True

    time_2 = flask.g.request_time()
    data['Total_time_taken'] = time_2
        
    # return response in json format 
    return flask.jsonify(data)    

def main():
    # start the flask app (allow remote connections) 
    app.run(host = '0.0.0.0', port = 9000)    
    
    # exit without errors
    sys.exit(0)
    
if __name__ == '__main__':
    main()
