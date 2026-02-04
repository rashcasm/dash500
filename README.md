# Nifty 500 Dashboard

A web-based financial dashboard for visualizing NIFTY 500 stock market data. This application fetches real-time historical candlestick data from the Upstox API and displays interactive price charts for 500 Indian stocks.

## Features

- **Real-time Data Fetching**: Download historical OHLCV (Open, High, Low, Close, Volume) data from Upstox API
- **Multiple Timeframes**: Support for daily, weekly, and monthly candlestick data
- **Interactive Charts**: View candlestick charts with zoom and hover capabilities using Plotly
- **500 Stocks Coverage**: Pre-configured with all NIFTY 500 stocks
- **Date Range Selection**: Flexible date range filtering for historical data analysis
- **Web-based Interface**: Clean, responsive UI for easy stock browsing and charting

## Installation

1. **Clone or download the project**:
   ```bash
   git clone <repository-url>
   cd niftydashboard
   ```
   Or download as ZIP and extract the folder.

2. **Create a Python virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate
   # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Add your Upstox API Access Token**:
   - Open `app.py` and paste your token:
     ```python
     ACCESS_TOKEN = 'your_token_here'
     ```

5. **Run the application**:
   ```bash
   python app.py
   ```
   Open your browser and go to `http://localhost:5000`
