import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
import tensorflow as tf
from keras.models import load_model
from keras.initializers import Orthogonal
import yfinance as yf

# download the data
data = yf.download('TSLA', start='2025-01-30', end = '2025-03-15', interval='30m')

# save the data in csv file
data.to_csv('data.csv')

# load the data
data = pd.read_csv('data.csv')

# load the dataset
# data = pd.read_csv('tesla_data.csv')
# data = pd.read_csv('apple_data.csv')

data = pd.DataFrame(data)

# features of data
features = ['Close', 'High', 'Low', 'Open', 'Volume']

data = data[features]

data['Close'] = pd.to_numeric(data['Close'], errors='coerce')

# include price change (returns)
data['Returns'] = data['Close'].pct_change()

# Relative Strength Index (RSI)
delta = data['Close'].diff()
gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
rs = gain / loss
data['RSI'] = 100 - (100 / (1 + rs))

# Moving Average Convergence Divergence (MACD)
exp1 = data['Close'].ewm(span=12, adjust=False).mean()
exp2 = data['Close'].ewm(span=26, adjust=False).mean()
data['MACD'] = exp1 - exp2

# Bollinger Bands
data['Rolling Mean'] = data['Close'].rolling(window=20).mean()
data['Rolling Std'] = data['Close'].rolling(window=20).std()
data['Upper Band'] = data['Rolling Mean'] + (data['Rolling Std'] * 2)
data['Lower Band'] = data['Rolling Mean'] - (data['Rolling Std'] * 2)

# Convert to numeric values, coercing any errors to NaN
data['High'] = pd.to_numeric(data['High'], errors='coerce')
data['Low'] = pd.to_numeric(data['Low'], errors='coerce')
data['Close'] = pd.to_numeric(data['Close'], errors='coerce')

# Now compute ATR
high_low = data['High'] - data['Low']
high_close = np.abs(data['High'] - data['Close'].shift())
low_close = np.abs(data['Low'] - data['Close'].shift())
data['TR'] = np.maximum(high_low, np.maximum(high_close, low_close))
data['ATR'] = data['TR'].rolling(window=14).mean()
processed_data = data.dropna()

# features
features = ['Close', 'Open', 'High', 'Low', 'Volume', 'Returns', 'RSI', 'MACD', 'Upper Band', 'Lower Band', 'ATR']

# define a scalar
scaler = MinMaxScaler(feature_range=(0, 1))
scaled_data = scaler.fit_transform(processed_data[features])

df_scaled = pd.DataFrame(scaled_data, columns=features, index=processed_data.index)

print(df_scaled.shape)

print("Hello World")
# Load the model
# model = load_model('lstm_stock_model.keras', custom_objects={'Orthogonal': Orthogonal})
model = load_model('lstm_model.h5', custom_objects={'Orthogonal': Orthogonal})

# define a create_sequence for 60 day
def create_sequence(data, seq_length):
    X = []
    for i in range(len(data) - seq_length):
        X.append(data[i:i + seq_length])
    return np.array(X)


# Function to predict if the price will go up or down
def predict_price_direction(data):
    # Ensure data is a numpy array and reshape it for LSTM input (samples, timesteps, features)
    data = data.reshape(1, data.shape[0], data.shape[1])
    # Get the prediction from the LSTM model (sigmoid output)
    prediction = model.predict(data)
    
    # Convert to direction
    direction = 'up' if prediction > 0.5 else 'down'
    return direction

data = create_sequence(df_scaled.values, 60)

# # Loop through each sequence and predict the direction
for i in range(10):  # loop through all sequences
    direction = predict_price_direction(data[i])  # Predict the direction for each sequence
    print(f"Prediction for sequence {i}: {direction}")

# predict the first and last sequence
print(f"Prediction for first sequence: {predict_price_direction(data[0])}")
print(f"Prediction for last sequence: {predict_price_direction(data[-1])}")