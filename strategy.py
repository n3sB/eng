from indicators import calculate_rsi, calculate_macd

def evaluate_strategy(symbol, closes, config, position):
    rsi = calculate_rsi(closes, config.RSI_PERIOD)
    macd_hist = calculate_macd(closes)[2]

    if len(closes) > config.RSI_PERIOD:
        last_rsi = rsi[-1]
        last_macd_hist = macd_hist[-1]

        if last_rsi < config.RSI_OVERSOLD and last_macd_hist > 0 and not position['in_position']:
            return "BUY"
        elif last_rsi > config.RSI_OVERBOUGHT and last_macd_hist < 0 and position['in_position']:
            return "SELL"
    return "HOLD"
