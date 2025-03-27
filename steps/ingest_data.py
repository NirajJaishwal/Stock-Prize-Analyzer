import yfinance as yf
import logging

# function to download data
def download_data(stock, start_date, end_date, interval):
    try:
        data = yf.download(stock, start=start_date, end=end_date, interval=interval)
        return data
    except Exception as e:
        logging.error(e)
        return "Error in the data download"