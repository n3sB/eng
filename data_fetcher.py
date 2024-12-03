import websocket, json
from binance.client import Client
import config

client = Client(config.API_KEY, config.API_SECRET)

def fetch_historical_data(symbol, interval, lookback):
    """Fetch historical klines."""
    klines = client.get_historical_klines(symbol, interval, lookback)
    return klines

def on_message(ws, message, process_candle):
    """Handle incoming WebSocket messages."""
    json_message = json.loads(message)
    if 'k' in json_message:  # Candle data
        symbol = json_message['s']
        candle = json_message['k']
        is_candle_closed = candle['x']
        close = float(candle['c'])

        if is_candle_closed:
            process_candle(symbol, close)

def start_stream(process_candle):
    """Start the WebSocket stream."""
    symbols_stream = "/".join([f"{symbol.lower()}@kline_1m" for symbol in config.TRADE_SYMBOLS])
    socket = f"wss://stream.binance.com:9443/ws/{symbols_stream}"

    ws = websocket.WebSocketApp(socket, on_message=lambda ws, msg: on_message(ws, msg, process_candle))
    ws.run_forever()