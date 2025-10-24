import argparse
from binance.error import ClientError  # <-- CORRECTED IMPORT
from src.client import client
from src.logger import log

def place_stop_limit_order(symbol, side, quantity, stop_price, price):
    """
    Places a STOP_LIMIT order on Binance Futures.
    """
    if not client:
        log.error("Client not initialized. Exiting stop-limit order.")
        return

    try:
        # 1. Input Validation
        symbol = symbol.upper()
        side = side.upper()
        quantity = float(quantity)
        price = float(price)
        stop_price = float(stop_price)

        if side not in ['BUY', 'SELL']:
            log.error(f"Invalid side: {side}. Must be 'BUY' or 'SELL'.")
            return
        
        if quantity <= 0 or price <= 0 or stop_price <= 0:
            log.error(f"Invalid quantity/price: {quantity}/{price}/{stop_price}. Must be positive.")
            return

        log.info(f"Attempting to place STOP_LIMIT {side} order for {quantity} {symbol}...")
        log.info(f"  Trigger (Stop) Price: {stop_price}, Limit Price: {price}")

        # 2. Place Order
        order = client.new_order(
            symbol=symbol,
            side=side,
            type='STOP', # 'STOP' is an alias for 'STOP_LIMIT' on futures
            quantity=quantity,
            price=price,            # The price for the limit order
            stopPrice=stop_price,   # The trigger price
            timeInForce='GTC'
        )
        
        # 3. Log Execution
        log.info(f"STOP_LIMIT order placed successfully. OrderID: {order['orderId']}")
        log.debug(order)

    except ClientError as e:  # <-- CORRECTED EXCEPTION
        # 3. Log Error
        log.error(f"Error placing stop-limit order for {symbol}: {e.error_message}")
    except ValueError:
        log.error(f"Invalid quantity/price. Check inputs.")
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Example usage: python -m src.advanced.stop_limit BTCUSDT SELL 0.01 59000 58950
    parser = argparse.ArgumentParser(description='Place a Binance Futures Stop-Limit Order')
    parser.add_argument('symbol', type=str, help='Trading symbol (e.g., BTCUSDT)')
    parser.add_argument('side', type=str, choices=['BUY', 'SELL'], help='Order side (BUY or SELL)')
    parser.add_argument('quantity', type=str, help='Order quantity')
    parser.add_argument('stop_price', type=str, help='Stop trigger price')
    parser.add_argument('price', type=str, help='Limit execution price')
    
    args = parser.parse_args()
    
    place_stop_limit_order(args.symbol, args.side, args.quantity, args.stop_price, args.price)
