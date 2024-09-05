import datetime
import dash
from dash import Dash, dcc, html, Input, Output, callback
import plotly.graph_objs as go
import pandas as pd
import yfinance as yahooFinance
from apscheduler.schedulers.background import BackgroundScheduler
from dash.dependencies import Input, Output
from pymongo import MongoClient

# Initialize Dash app
app = Dash(__name__)

# External Stylesheets
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Scheduler to fetch stock data periodically
scheduler = BackgroundScheduler()
scheduler.start()

# Global variable to store stock data
df = pd.DataFrame()

def fetch_stock_data():
    global df
    
    # Connect to MongoDB
    username = "fernando35687"
    password = "H1qMQ351jL1ujpMC" 
    connection_string = "mongodb+srv://fernando35687:H1qMQ351jL1ujpMC@cluster0.mlldx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
    client = MongoClient(connection_string)
    db = client['stock_data_db']
    collection = db['meta_stock_prices']
    
    # Calculate the start date (6 months ago) and end date (now)
    end_date = datetime.datetime.now()
    start_date = end_date - datetime.timedelta(days=6*30)  # Approx 6 months
    
    # Query MongoDB for data within the date range
    query = {
        'Date': {
            '$gte': start_date,
            '$lte': end_date
        }
    }
    
    # Fetch data from MongoDB
    stock_data = list(collection.find(query))
    
    # Check if stock_data is empty
    if not stock_data:
        print("No data found for the specified date range.")
        return

    # Convert the list of dictionaries to a DataFrame
    df = pd.DataFrame(stock_data)
    
    # Ensure the 'Date' column is in datetime format
    df['Date'] = pd.to_datetime(df['Date'])
    
    # Reset index if necessary
    df.reset_index(drop=True, inplace=True)
    

# Call the function to test
fetch_stock_data()


fetch_stock_data()
scheduler.add_job(fetch_stock_data, 'interval', minutes=1)

app.layout = html.Div([
    html.H4('META Stock Prices Live Feed'),
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=1*60*1000,  # 1 minute in milliseconds
        n_intervals=0
    )
])

@callback(Output('live-update-graph', 'figure'),
          Input('interval-component', 'n_intervals'))
def update_graph_live(n):
    # Ensure data is updated
    fetch_stock_data()

    # Create the graph
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=df['Date'],
        y=df['Close'],
        mode='lines+markers',
        name='Close Price'
    ))

    fig.update_layout(
        title='META Stock Prices',
        xaxis_title='Date',
        yaxis_title='Close Price',
        xaxis_rangeslider_visible=True
    )

    return fig

if __name__ == '__main__':
    app.run(debug=True)
