def check_risk(close, position, config):
    """Check stop-loss and take-profit."""
    if position['in_position']:
        entry_price = position['buy_price']
        if close <= entry_price * (1 - config.STOP_LOSS_PERCENT):
            return "SELL_STOP_LOSS"
        elif close >= entry_price * (1 + config.TAKE_PROFIT_PERCENT):
            return "SELL_TAKE_PROFIT"
    return "HOLD"
