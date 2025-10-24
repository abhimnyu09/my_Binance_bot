import argparse
from binance.error import ClientError  # <-- CORRECTED IMPORT
from src.client import client
from src.logger import log

def place_limit_order(symbol, side, quantity, price):
    """
    Places a limit order on Binance Futures.
    """
    if not client:
        log.error("Client not initialized. Exiting limit order.")
        return

    try:
        # 1. Input Validation
        symbol = symbol.upper()
        side = side.upper()
        quantity = float(quantity)
        price = float(price)

        if side not in ['BUY', 'SELL']:
            log.error(f"Invalid side: {side}. Must be 'BUY' or 'SELL'.")
            return
        
        if quantity <= 0 or price <= 0:
            log.error(f"Invalid quantity/price: {quantity}/{price}. Must be positive.")
            return

        log.info(f"Attempting to place LIMIT {side} order for {quantity} {symbol} at {price}...")

        # 2. Place Order
        order = client.new_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            quantity=quantity,
            price=price,
            timeInForce='GTC'  # Good 'Til Canceled
        )
        
        # 3. Log Execution
        log.info(f"LIMIT order placed successfully. OrderID: {order['orderId']}")
        log.debug(order)

    except ClientError as e:  # <-- CORRECTED EXCEPTION
        # 3. Log Error
        log.error(f"Error placing limit order for {symbol}: {e.error_message}")
    except ValueError:
        log.error(f"Invalid quantity/price: {quantity}/{price}. Must be valid numbers.")
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Example usage: python -m src.limit_orders BTCUSDT BUY 0.01 50000
    parser = argparse.ArgumentParser(description='Place a Binance Futures Limit Order')
    parser.add_argument('symbol', type=str, help='Trading symbol (e.g., BTCUSDT)')
    parser.add_argument('side', type=str, choices=['BUY', 'SELL'], help='Order side (BUY or SELL)')
    parser.add_argument('quantity', type=str, help='Order quantity (e.g., 0.01)')
    parser.add_argument('price', type=str, help='Order price (e.g., 50000)')
    
    args = parser.parse_args()
    
    place_limit_order(args.symbol, args.side, args.quantity, args.price)
