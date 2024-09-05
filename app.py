from flask import Flask, jsonify
import yfinance as yahooFinance
import datetime
import pymongo
from apscheduler.schedulers.background import BackgroundScheduler
from bson import json_util
import json
from pymongo import MongoClient

# Initialize Flask app
app = Flask(__name__)

# MongoDB connection (Replace <username>, <password>, <cluster-url> with your actual MongoDB details)
username = "fernando35687"
password = "H1qMQ351jL1ujpMC"
connection_string = "mongodb+srv://fernando35687:H1qMQ351jL1ujpMC@cluster0.mlldx.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client = MongoClient(connection_string)
db = client['stock_data_db']
collection = db['meta_stock_prices']

# Scheduler to run tasks
scheduler = BackgroundScheduler()

# Function to fetch stock data
def fetch_and_store_stock_data():
    print("Fetching and updating stock data...")
    
    # Fetch stock data
    meta_stock = yahooFinance.Ticker("META")
    start_date = datetime.datetime.now() - datetime.timedelta(days=1)  # Fetching data for the past 1 day
    end_date = datetime.datetime.now()
    stock_data = meta_stock.history(start=start_date, end=end_date)
    
    # Convert stock data to dictionary
    stock_data_dict = stock_data.to_dict('records')

    # Insert into MongoDB (if updating, ensure handling duplication, e.g., using upsert)
    if stock_data_dict:
        collection.insert_many(stock_data_dict)
    print("Stock data updated successfully.")

# Schedule the task to fetch stock data every minute
scheduler.add_job(fetch_and_store_stock_data, 'interval', minutes=1)
scheduler.start()

@app.route('/get_data', methods=['GET'])
def get_data():
    # Get the most recent stock data from MongoDB
    stock_data = collection.find().sort([('_id', pymongo.DESCENDING)]).limit(10)  # Example: Get last 10 records
    stock_data_json = json.loads(json_util.dumps(stock_data))  # Convert to JSON format
    return jsonify(stock_data_json)

if __name__ == '__main__':
    # Fetch stock data every minute and update MongoDB
    app.run(debug=True)