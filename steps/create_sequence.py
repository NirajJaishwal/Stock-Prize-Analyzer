import numpy as np
import logging
from flask import jsonify

# Function to create squeunce of data
def create_sequence(data, seq_length):
    try:
        X = []
        for i in range(len(data) - seq_length):
            X.append(data[i:i + seq_length])
        return np.array(X)
    except Exception as e:
        logging.error(f"Error in create_sequence: {e}")
        return None
