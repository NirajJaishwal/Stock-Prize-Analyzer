from keras.models import load_model
from keras.initializers import Orthogonal
import logging

# select model based on the time interval
def select_model(interval):
    """
    Function to select the model based on the time interval.
    
    Parameters:
    interval: Time interval for the model selection
    
    Returns:
    model: Loaded LSTM model
    """
    try:
        if interval == '15m':
            model = load_model('model/lstm_model_30m.h5', custom_objects={'Orthogonal': Orthogonal})
        elif interval == '30m':
            model = load_model('model/lstm_model_30m.h5', custom_objects={'Orthogonal': Orthogonal})
        elif interval == '60m':
            model = load_model('model/lstm_model_1h.keras', custom_objects={'Orthogonal': Orthogonal})
        elif interval == '1d':
            model = load_model('model/lstm_model_30m.h5', custom_objects={'Orthogonal': Orthogonal})
        else:
            raise ValueError("Invalid time interval")
        
        return model
    except Exception as e:
        logging.error(f"Error in select_model: {e}")
        return None
