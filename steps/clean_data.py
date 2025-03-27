import yfinance as yf

# function to download data
def download_data(stock, start_date, end_date, interval):
    data = yf.download(stock, start=start_date, end=end_date, interval=interval)
    return data