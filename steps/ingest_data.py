import yfinance as yf
import logging
from flask import jsonify

# function to download data
def download_data(stock, start_date, end_date, interval):
    try:
        data = yf.download(stock, start=start_date, end=end_date, interval=interval)
        return data
    except Exception as e:
        logging.error(f"Error downloading data: {e}")
        return None
