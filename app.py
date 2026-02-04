import os
import time
import pandas as pd
from flask import Flask, render_template, request, jsonify
import upstox_client
from upstox_client.rest import ApiException

app = Flask(__name__)

# --- CONFIGURATION ---
# In a real app, you'd handle auth better, but for this local tool:
ACCESS_TOKEN = ''  # <--- PASTE YOUR TOKEN HERE
KEYS_FILE = 'nifty500_keys.csv'

# Configure Upstox API
configuration = upstox_client.Configuration()
configuration.access_token = ACCESS_TOKEN
api_instance = upstox_client.HistoryV3Api(upstox_client.ApiClient(configuration))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/fetch-data', methods=['POST'])
def fetch_data():
    """Triggers the download loop based on UI input"""
    data = request.json
    timeframe = data.get('timeframe') # 'daily', 'weekly', 'monthly'
    start_date = data.get('startDate')
    end_date = data.get('endDate')
    
    # 1. Setup Folders & Timeframe Map
    output_folder = f"data_{timeframe}"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    tf_map = {
        'daily':   {'unit': 'days',   'interval': '1'},
        'weekly':  {'unit': 'weeks',  'interval': '1'},
        'monthly': {'unit': 'months', 'interval': '1'}
    }
    
    unit_param = tf_map[timeframe]['unit']
    interval_param = tf_map[timeframe]['interval']
    
    # 2. Load Keys
    if not os.path.exists(KEYS_FILE):
        return jsonify({"status": "error", "message": "Keys file not found!"})
        
    df_keys = pd.read_csv(KEYS_FILE)
    success_count = 0
    downloaded_stocks = []

    # 3. The Download Loop (Simplified for speed in demo)
    # NOTE: Fetching 500 stocks takes time (~30-60s). The UI will spin while this runs.
    for index, row in df_keys.iterrows():
        symbol = row['Symbol']
        key = row['Instrument_Key']
        
        try:
            response = api_instance.get_historical_candle_data1(
                instrument_key=key,
                unit=unit_param,
                interval=interval_param,
                to_date=end_date,
                from_date=start_date
            )

            if response.data and response.data.candles:
                candles = response.data.candles
                cols = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'OI']
                df = pd.DataFrame(candles, columns=cols)
                
                # Clean & Save
                df['Timestamp'] = pd.to_datetime(df['Timestamp'])
                df = df.sort_values('Timestamp', ascending=True).reset_index(drop=True)
                
                save_path = f"{output_folder}/{symbol}.csv"
                df.to_csv(save_path, index=False)
                
                success_count += 1
                downloaded_stocks.append(symbol)
            
            # Rate limit
            time.sleep(0.05) 

        except Exception as e:
            print(f"Skipping {symbol}: {e}")
            continue

    return jsonify({
        "status": "success", 
        "message": f"Downloaded {success_count} stocks.",
        "stocks": downloaded_stocks,
        "folder": output_folder
    })

@app.route('/get-chart-data', methods=['POST'])
def get_chart_data():
    """Reads a specific CSV and sends data to frontend"""
    req = request.json
    symbol = req.get('symbol')
    folder = req.get('folder')
    
    file_path = f"{folder}/{symbol}.csv"
    
    if os.path.exists(file_path):
        df = pd.read_csv(file_path)
        # Convert to list of dicts for JSON
        return df.to_json(orient='records')
    else:
        return jsonify({"error": "File not found"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)