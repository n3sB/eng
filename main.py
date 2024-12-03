import config
from data_fetcher import start_stream
from strategy import evaluate_strategy
from risk_management import check_risk
from order_executor import execute_order

# State management
closes = {symbol: [] for symbol in config.TRADE_SYMBOLS}
positions = {symbol: {'in_position': False, 'buy_price': None} for symbol in config.TRADE_SYMBOLS}

def process_candle(symbol, close):
    global closes, positions

    closes[symbol].append(close)

    if len(closes[symbol]) > config.RSI_PERIOD:
        closes[symbol] = closes[symbol][-config.RSI_PERIOD * 2:]  # Trim data

        # Check strategy signals
        action = evaluate_strategy(symbol, closes[symbol], config, positions[symbol])

        # Risk management
        if positions[symbol]['in_position']:
            risk_action = check_risk(close, positions[symbol], config)
            if risk_action in ["SELL_STOP_LOSS", "SELL_TAKE_PROFIT"]:
                action = "SELL"

        if action == "BUY":
            if execute_order(client, symbol, SIDE_BUY, config.TRADE_QUANTITY):
                positions[symbol]['in_position'] = True
                positions[symbol]['buy_price'] = close
        elif action == "SELL":
            if execute_order(client, symbol, SIDE_SELL, config.TRADE_QUANTITY):
                positions[symbol]['in_position'] = False
                positions[symbol]['buy_price'] = None

if __name__ == "__main__":
    start_stream(process_candle)
