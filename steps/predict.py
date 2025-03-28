import logging
from flask import jsonify, render_template

from steps.create_sequence import create_sequence
from steps.predict_data import predict_price_direction

def make_prediction(model, data, seq_length):
    try:
        sequences = create_sequence(data.values, seq_length)

        # check if the sequence has data
        if sequences is None or len(sequences) == 0:
            return None,"Not enough data to make prediction"

        last_pred = predict_price_direction(model, sequences[-1])
        return last_pred, None
    except Exception as e:
        logging.error(f'Error in predict:{e}')
        return None, f'An error occured: {str(e)}'
