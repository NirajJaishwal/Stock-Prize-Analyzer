import logging
from flask import jsonify

# Function to predict data using a trained model
def predict_price_direction(model, sequences):
    """
    Function to predict the price direction using the trained model.

    Parameters:
    model: Trained LSTM model
    sequences: Input data sequences

    Returns:
    direction: Predicted price direction ('High' or 'Low')
    """
    try:
        # Ensure data is a numpy array and reshape it for LSTM input (samples, timesteps, features)
        sequences = sequences.reshape(1, sequences.shape[0], sequences.shape[1])
        # Get the prediction from the LSTM model (sigmoid output)
        prediction = model.predict(sequences)
        # Convert to direction
        direction = 'High' if prediction > 0.5 else 'Low'
        return direction
    except Exception as e:
        logging.error(f"Error in predict_data: {e}")
        return jsonify({'error': 'Prediction failed'}), 500
