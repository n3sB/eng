from binance.enums import *

def execute_order(client, symbol, side, quantity):
    """Place an order."""
    try:
        print(f"Placing {side} order for {symbol}")
        order = client.create_order(symbol=symbol, side=side, type=ORDER_TYPE_MARKET, quantity=quantity)
        print(order)
    except Exception as e:
        print(f"Order failed: {e}")
        return False
    return True
