from flask import Flask, request, jsonify, render_template
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras.models import load_model
from keras.initializers import Orthogonal

from steps.ingest_data import download_data
from steps.draw_graph import draw_graph
from steps.clean_data import cleanData

app = Flask(__name__)

# Load the model
model = load_model('lstm_model.h5', custom_objects={'Orthogonal': Orthogonal})

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

    if data.empty:
        return jsonify({'error': 'No data found for the given stock'}), 400
    
    # draw the graph of closing price
    graph = draw_graph(data, stock)
    
    # save into csv file it the file name exist replace it
    data.to_csv('data.csv')
    
    # load the data
    data = pd.read_csv('data.csv')  

    # clean the data
    processed_data = cleanData(data)

    # features
    features = ['Close', 'Open', 'High', 'Low', 'Volume', 'Returns', 'RSI', 'MACD', 'Upper Band', 'Lower Band', 'ATR']

    # define a scalar
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(processed_data[features])

    df_scaled = pd.DataFrame(scaled_data, columns=features, index=processed_data.index)

    print(df_scaled.shape)

    # define a create_sequence for 60 day
    def create_sequence(data, seq_length=60):
        X = []
        for i in range(len(data) - seq_length):
            X.append(data[i:i + seq_length])
        return np.array(X)

    sequences = create_sequence(df_scaled.values)

    # Function to predict if the price will go up or down
    def predict_price_direction(sequence):
        # Ensure data is a numpy array and reshape it for LSTM input (samples, timesteps, features)
        sequence = sequence.reshape(1, sequence.shape[0], sequence.shape[1])
        # Get the prediction from the LSTM model (sigmoid output)
        prediction = model.predict(sequence)
        # Convert to direction
        direction = 'High' if prediction > 0.5 else 'Low'
        return direction
    
    # first_pred = predict_price_direction(sequences[0])
    last_pred = predict_price_direction(sequences[-1])

    return render_template('index.html', 
                            last_prediction=last_pred,
                            graph_html=graph)

if __name__ == '__main__':
    app.run(debug=True)