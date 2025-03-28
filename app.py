from flask import Flask, request, jsonify, render_template
import pandas as pd
from keras.models import load_model
from keras.initializers import Orthogonal

from steps.ingest_data import download_data
from steps.draw_graph import draw_graph
from steps.clean_data import cleanData
from steps.predict import make_prediction

app = Flask(__name__)

# Load the model
model = load_model('model/lstm_model.h5', custom_objects={'Orthogonal': Orthogonal})

@app.route('/')
def home():
    return render_template('index.html', graph_html=None)

@app.route('/predict', methods=['POST'])
def predict():
    # get the data from the form
    stock = request.form['stockSymbol']
    start_date = request.form['startDate']
    end_date = request.form['endDate']
    interval = request.form['interval']
    
    # if date is not available return error
    if not start_date or not end_date or not interval or not stock:
        return jsonify({'error': 'All fields are required'}),400

    # load the data from ingest_data
    data = download_data(stock, start_date, end_date, interval)

    # draw the graph of closing price
    graph = draw_graph(data, stock)
    
    # save into csv file it the file name exist replace it
    data.to_csv('data/data.csv')
    
    # load the data
    data = pd.read_csv('data/data.csv')  

    # clean the data
    df_scaled = pd.DataFrame(cleanData(data))

    last_pred, error_msg = make_prediction(model, df_scaled, 60)

    if error_msg == None:
        # return render_template('index.html',
        #                         last_prediction=last_pred,
        #                         graph_html=graph)
        return render_template('result.html',
                                last_prediction=last_pred,
                                graph_html=graph)
    else:
        return render_template('error.html', error_message=error_msg)

if __name__ == '__main__':
    app.run(debug=True)
