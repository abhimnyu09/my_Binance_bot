import os
from binance.um_futures import UMFutures
from binance.error import ClientError  # <-- CORRECTED IMPORT
from dotenv import load_dotenv
from src.logger import log

# Load environment variables from .env file
load_dotenv()

def get_binance_client():
    """
    Initializes and returns an authenticated Binance USDT-M Futures client.
    """
    api_key = os.getenv('API_KEY')
    api_secret = os.getenv('API_SECRET')

    if not api_key or not api_secret or api_key == 'YOUR_BINANCE_API_KEY_GOES_HERE':
        log.error("API_KEY or API_SECRET not set in the .env file.")
        log.info("Please create a .env file and add your API keys.")
        return None

    try:
        # --- IMPORTANT ---
        # For testing, use the Testnet URL
        client = UMFutures(key=api_key, secret=api_secret, base_url="https://testnet.binancefuture.com")
        
        # For live trading, comment out the line above and uncomment the line below
        # client = UMFutures(key=api_key, secret=api_secret)
        
        # Check connection
        client.ping()
        log.info("Binance Futures Testnet client connected successfully.")
        return client
    except ClientError as e:  # <-- CORRECTED EXCEPTION
        log.error(f"Failed to connect to Binance API: {e}")
        return None
    except Exception as e:
        log.error(f"An unexpected error occurred during client initialization: {e}")
        return None

# Create a single client
