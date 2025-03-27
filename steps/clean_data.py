# import pandas as pd
# import numpy as np

# # clean the data
# def cleanData(data):
#     data = pd.DataFrame(data)
    
#     # features of data
#     features = ['Close', 'High', 'Low', 'Open', 'Volume']
    
#     data = data[features]
    
#     data['Close'] = pd.to_numeric(data['Close'], errors='coerce')
    
#     # include price change (returns)
#     data['Returns'] = data['Close'].pct_change()
    
#     # Relative Strength Index (RSI)
#     delta = data['Close'].diff()
#     gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
#     loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
#     rs = gain / loss
#     data['RSI'] = 100 - (100 / (1 + rs))
    
#     # Moving Average Convergence Divergence (MACD)
#     exp1 = data['Close'].ewm(span=12, adjust=False).mean()
#     exp2 = data['Close'].ewm(span=26, adjust=False).mean()
#     data['MACD'] = exp1 - exp2
    
#     # Bollinger Bands
#     data['Rolling Mean'] = data['Close'].rolling(window=20).mean()
#     data['Rolling Std'] = data['Close'].rolling(window=20).std()
#     data['Upper Band'] = data['Rolling Mean'] + (data['Rolling Std'] * 2)
#     data['Lower Band'] = data['Rolling Mean'] - (data['Rolling Std'] * 2)
    
#     # Convert to numeric values, coercing any errors to NaN
#     data['High'] = pd.to_numeric(data['High'], errors='coerce')
#     data['Low'] = pd.to_numeric(data['Low'], errors='coerce')
#     data['Close'] = pd.to_numeric(data['Close'], errors='coerce')

#     # Now compute ATR
#     high_low = data['High'] - data['Low']
#     high_close = np.abs(data['High'] - data['Close'].shift())
#     low_close = np.abs(data['Low'] - data['Close'].shift())
#     data['TR'] = np.maximum(high_low, np.maximum(high_close, low_close))
#     data['ATR'] = data['TR'].rolling(window=14).mean()
#     processed_data = data.dropna()

#     # features
#     features = ['Close', 'Open', 'High', 'Low', 'Volume', 'Returns', 'RSI', 'MACD', 'Upper Band', 'Lower Band', 'ATR']
