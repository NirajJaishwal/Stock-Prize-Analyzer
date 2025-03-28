import plotly.express as px
import plotly.io as pio
import logging
from flask import jsonify

# Draw graph 
def draw_graph(data, stock):
    try:
        fig = px.line(data, x=data.index, y=data['Close'].values.flatten(), title='Closing Price of ' + stock)
        graph = pio.to_html(fig, full_html=False)
        return graph
    except Exception as e:
        logging.error(e)
        return jsonify({'error': 'Graph generation failed'}), 500
