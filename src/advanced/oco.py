import argparse
from binance.error import ClientError  # <-- CORRECTED IMPORT
from src.client import client
from src.logger import log

def place_oco_order(symbol, side, quantity, price, stop_price):
    """
    Simulates an OCO (One-Cancels-the-Other) order for an existing position
    by placing two separate 'reduceOnly' orders:
    1. A LIMIT order (Take Profit)
    2. A STOP_MARKET order (Stop Loss)
    
    This example assumes you are placing a SELL OCO for an existing LONG position.
    """
    if not client:
        log.error("Client not initialized. Exiting OCO order.")
        return

    if side.upper() != 'SELL':
        log.error("This OCO example is for a SELL side (TP/SL on a LONG position).")
        return

    try:
        # 1. Input Validation
        symbol = symbol.upper()
        side = side.upper()
        quantity = float(quantity)
        price = float(price) # Take-profit price
        stop_price = float(stop_price) # Stop-loss trigger price

        if quantity <= 0 or price <= 0 or stop_price <= 0:
            log.error(f"Invalid inputs: All values must be positive.")
            return

        log.info(f"Attempting to place OCO {side} order for {quantity} {symbol}...")
        log.info(f"  Take Profit at: {price}")
        log.info(f"  Stop Loss at: {stop_price}")
        
        # 2. Place Take-Profit LIMIT order
        tp_order = client.new_order(
            symbol=symbol,
            side=side,
            type='LIMIT',
            quantity=quantity,
            price=price,
            timeInForce='GTC',
            reduceOnly='true' # Ensures it only closes a position
        )
        log.info(f"Take-Profit LIMIT order placed. OrderID: {tp_order['orderId']}")

        # 3. Place Stop-Loss STOP_MARKET order
        sl_order = client.new_order(
            symbol=symbol,
            side=side,
            type='STOP_MARKET',
            quantity=quantity,
            stopPrice=stop_price,
            reduceOnly='true' # Ensures it only closes a position
        )
        log.info(f"Stop-Loss STOP_MARKET order placed. OrderID: {sl_order['orderId']}")
        
        log.info("OCO (TP/SL) orders placed successfully.")

    except ClientError as e:  # <-- CORRECTED EXCEPTION
        log.error(f"Error placing OCO orders for {symbol}: {e.error_message}")
        # Note: You might need to cancel the first order if the second one fails
    except ValueError:
        log.error(f"Invalid quantity/price. Check inputs.")
    except Exception as e:
        log.error(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    # Example: python -m src.advanced.oco BTCUSDT SELL 0.01 65000 59000
    parser = argparse.ArgumentParser(description='Place a Futures OCO (TP/SL) Order')
    parser.add_argument('symbol', type=str, help='Trading symbol (e.g., BTCUSDT)')
    parser.add_argument('side', type=str, choices=['SELL'], help='Order side (must be SELL for this TP/SL example)')
    parser.add_argument('quantity', type=str, help='Order quantity (must match position)')
    parser.add_argument('price', type=str, help='Take-Profit limit price')
    parser.add_argument('stop_price', type=str, help='Stop-Loss trigger price')
    
    args = parser.parse_args()
    
    place_oco_order(args.symbol, args.side, args.quantity, args.price, args.stop_price)
