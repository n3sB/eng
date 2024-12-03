import websocket, json
from binance.client import Client
import config

client = Client(config.API_KEY, config.API_SECRET)

def fetch_historical_data(symbol, interval):
    start_date = (datetime.now(timezone.utc) - timedelta(days=120)).strftime('%Y-%m-%d %H:%M:%S')
    klines = client.get_historical_klines(symbol, interval, start_date)
    return klines

def on_message(ws, message, process_candle):
    json_message = json.loads(message)
    if 'k' in json_message:  # Candle data
        symbol = json_message['s']
        candle = json_message['k']
        is_candle_closed = candle['x']
        close = float(candle['c'])

        if is_candle_closed:
            process_candle(symbol, close)

def start_stream(process_candle):
    symbols_stream = "/".join([f"{symbol.lower()}@kline_1m" for symbol in config.TRADE_SYMBOLS])
    socket = f"wss://stream.binance.com:9443/ws/{symbols_stream}"

    ws = websocket.WebSocketApp(socket, on_message=lambda ws, msg: on_message(ws, msg, process_candle))
    ws.run_forever()
