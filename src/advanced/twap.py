import argparse
import time
from binance.error import ClientError  # <-- CORRECTED IMPORT
from src.client import client
from src.logger import log

def execute_twap_strategy(symbol, side, total_quantity, duration_minutes):
    """
    Executes a simple TWAP (Time-Weighted Average Price) strategy.
    Splits the total quantity into 10 smaller chunks and executes one chunk
    every (duration / 10) minutes.
    """
    if not client:
        log.error("Client not initialized. Exiting TWAP strategy.")
        return

    try:
        # 1. Input Validation
        symbol = symbol.upper()
        side = side.upper()
        total_quantity = float(total_quantity)
        duration_minutes = int(duration_minutes)
        num_chunks = 10 # Split order into 10 smaller pieces

        if total_quantity <= 0 or duration_minutes <= 0:
            log.error("Quantity and duration must be positive.")
            return

        chunk_size = round(total_quantity / num_chunks, 8) # Round to 8 decimal places
        interval_seconds = (duration_minutes * 60) / num_chunks
        
        if chunk_size == 0:
            log.error("Total quantity is too small to be split into 10 chunks.")
            return

        log.info(f"Starting TWAP {side} strategy for {total_quantity} {symbol}...")
        log.info(f"  Duration: {duration_minutes} minutes")
        log.info(f"  Executing {chunk_size} {symbol} every {interval_seconds} seconds.")

        # 2. Execution Loop
        for i in range(num_chunks):
            log.info(f"Executing TWAP chunk {i+1}/{num_chunks}...")
            try:
                order = client.new_order(
                    symbol=symbol,
                    side=side,
                    type='MARKET',
                    quantity=chunk_size
                )
                log.info(f"  Chunk {i+1} placed. OrderID: {order['orderId']}")
            except ClientError as e:  # <-- CORRECTED EXCEPTION
                log.error(f"  Error placing TWAP chunk {i+1}: {e.error_message}")
            
            if i < num_chunks - 1:
                log.info(f"  Waiting {interval_seconds} seconds for next chunk...")
                time.sleep(interval_seconds)

        log.info("TWAP strategy execution complete.")

    except ValueError:
        log.error(f"Invalid quantity/duration. Must be valid numbers.")
    except Exception as e:
        log.error(f"An unexpected error occurred during TWAP: {e}")

if __name__ == "__main__":
    # Example: python -m src.advanced.twap BTCUSDT BUY 0.1 30
    # (Buys 0.1 BTC over 30 minutes)
    parser = argparse.ArgumentParser(description='Execute a TWAP Strategy')
    parser.add_argument('symbol', type=str, help='Trading symbol (e.g., BTCUSDT)')
    parser.add_argument('side', type=str, choices=['BUY', 'SELL'], help='Order side')
    parser.add_argument('quantity', type=str, help='Total order quantity')
    parser.add_argument('duration', type=int, help='Total duration in minutes')
    
    args = parser.parse_args()
    
    execute_twap_strategy(args.symbol, args.side, args.quantity, args.duration)
