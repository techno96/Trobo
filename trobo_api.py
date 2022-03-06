import time, flask, pickle, json, sys
#import pandas as pd
import numpy as np
from googleapiclient import discovery


# initialize flask object
app = flask.Flask(__name__)

#initialize API key for perpspective API
API_KEY = 'AIzaSyC4zu-biGJBTDft7HBOFzzqQrrTMa1-JIs'

# global dicts to store objects of TfidfVectorizer, MultiLabelBinarizer & trained model for each segment
vectorizer = {}
mlb = {}
model = {}

# global dict to store labels for classes in each segment
class_label_mapping = {}

# global list to store segments
segments = ['bsd', 'dhs', 'gen']

# compute model predictions using Perpective API
def compute_predictions(test_term):
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
    'requestedAttributes': {'FLIRTATION': {}, 'TOXICITY': {}, 'SEXUALLY_EXPLICIT': {}}
    }
   
    try:
        # retrun the rersponse from the Perspective API
        response = client.comments().analyze(body=analyze_request).execute()

        # declare the response labels
        labels = ['FLIRTATION', 'TOXICITY', 'SEXUALLY_EXPLICIT']

        # categorize the response labels
        flirtation = response['attributeScores']['FLIRTATION']['spanScores'][0]['score']['value']
        toxicity = response['attributeScores']['TOXICITY']['spanScores'][0]['score']['value']
        sexually_explicit = response['attributeScores']['SEXUALLY_EXPLICIT']['spanScores'][0]['score']['value']

        return labels[np.argmax(np.array([flirtation, toxicity, sexually_explicit]))]

    except Exception as exception:
        # return an invalid response
        return -1

# load class label mapping for each troll category
def load_class_label_mapping(prediction):
    # class_label_mapping used as global variable
    global class_label_mapping
    
    try:
        # load class label mapping from cached excel & convert to dict
        class_label_mapping_df = pd.read_excel('Class_Label_Mapping.xlsx', index_col = 0)
        class_label_mapping = class_label_mapping_df.to_dict('index')

    except Exception as exception:
        print('\n%s' % exception)
        sys.exit(0)

@app.before_request
def before_request():
    flask.g.request_start_time = time.time()
    flask.g.request_time = lambda: (time.time() - flask.g.request_start_time)

# define predict function as an endpoint 
@app.route('/predict', methods = ['GET'])
# serve predictions
def predict():
   # dict served on api call
    data = {'meme': [], 'joke': [], 'quote': [], 'success': False}

    # get request parameters
    params = flask.request.json
    if (params == None):
        params = flask.request.args

    # return classification results if parameters are found
    if (params != None):
        # initialize test term from params
        test_term = params.get('query')

        # initialize strategy from params
        strategy = params.get('strategy').lower()

        # compute model predictions using Perpective API
        prediction = compute_predictions(test_term)

        # load class label mapping for each troll strategy
        #load_class_label_mapping(prediction)
    
        # transform test term into Tfidf vector
        #X_pred = vectorizer[segment].transform([term_test])
        
        # predict probabilities for test term
        #prediction_probs = model[segment].predict(X_pred)[0]
        
        # store index of top n probabilities
        #sorted_prediction_indexes = np.argsort(prediction_probs)[::-1][:5]
    
        # store top n predictions (i.e. classes) based on a threshold
        #threshold = 0.3
        #predictions = [mlb[segment].classes_[index] for index in sorted_prediction_indexes if prediction_probs[index] >= threshold]

        time_1 = flask.g.request_time()
        
        # map classes in predictions to labels
        #labels = [class_label_mapping[segment][prediction] for prediction in predictions]

        # append predictions & labels to data
        #data['predictions'].extend(predictions)
        #data['labels'].extend(labels)
        data['prediction'] = prediction
        data['success'] = True

    time_2 = flask.g.request_time()
    #data['Time_taken_by_class_label_mapping'] = time_2 - time_1
    #data['Time_taken_without_class_label_mapping'] = time_1 
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
