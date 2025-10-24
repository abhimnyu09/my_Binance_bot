import argparse
from binance.error import ClientError  # <-- CORRECTED IMPORT
from src.client import client
from src.logger import log

def place_market_order(symbol, side, quantity):
    """
    Places a market order on Binance Futures.
    """
    if not client:
        log.error("Client not initialized. Exiting market order.")
        return

    try:
        # 1. Input Validation
        symbol = symbol.upper()
        side = side.upper()
        quantity = float(quantity)

        if side not in ['BUY', 'SELL']:
            log.error(f"Invalid side: {side}. Must be 'BUY' or 'SELL'.")
            return
        
        if quantity <= 0:
            log.error(f"Invalid quantity: {quantity}. Must be positive.")
            return

        log.info(f"Attempting to place MARKET {side} order for {quantity} {symbol}...")

        # 2. Place Order
        order = client.new_order(
            symbol=symbol,
            side=side,
            type='MARKET',
            quantity=quantity
        )
        
        # 3. Log Execution
        log.info(f"MARKET order placed successfully. OrderID: {order['orderId']}")
        log.debug(order) # Log full response for debugging

    except ClientError as e:  # <-- CORRECTED EXCEPTION
        # 3. Log Error
        log.error(f"Error placing market order for {symbol}: {e.error_message}")
    except ValueError:
        log.error(f"Invalid quantity: {quantity}. Must be a valid number.")
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Example usage: python -m src.market_orders BTCUSDT BUY 0.01
    parser = argparse.ArgumentParser(description='Place a Binance Futures Market Order')
    parser.add_argument('symbol', type=str, help='Trading symbol (e.g., BTCUSDT)')
    parser.add_argument('side', type=str, choices=['BUY', 'SELL'], help='Order side (BUY or SELL)')
    parser.add_argument('quantity', type=str, help='Order quantity (e.g., 0.01)')
    
    args = parser.parse_args()
    
    place_market_order(args.symbol, args.side, args.quantity)
