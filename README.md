# Binance Futures Order Bot

A CLI-based trading bot for the Binance USDT-M Futures market, built to satisfy the Python Developer assignment. It supports mandatory order types (Market, Limit) and several advanced, high-priority order types (Stop-Limit, OCO, TWAP).

The bot features robust input validation and comprehensive, structured logging for all actions, executions, and errors, which are saved to `bot.log`.

## 📁 Project Structure

The project directory is organized as specified in the assignment guidelines:

```
my_binance_bot/
│
├── .env                    # (Private) Your API keys are stored here
├── .gitignore              # (Important) Tells Git to ignore .env, logs, and venv
├── README.md               # (You are here) This setup and usage guide
├── requirements.txt        # List of Python libraries needed
├── bot.log                 # (Generated) All bot actions and errors are logged here
├── report.pdf              # (You must create) Your analysis and screenshots
│
└── src/                    # All Python source code
    │
    ├── client.py           # Handles API connection and authentication
    ├── logger.py           # Configures the 'bot.log' logger
    ├── market_orders.py    # Logic for Market orders
    ├── limit_orders.py     # Logic for Limit orders
    │
    └── advanced/           # Folder for bonus order types
        │
        ├── stop_limit.py   # Logic for Stop-Limit orders
        ├── oco.py          # Logic for OCO (One-Cancels-the-Other) orders
        └── twap.py         # Logic for TWAP (Time-Weighted Average Price) strategy
```

---

## 🚀 Step-by-Step Setup and Installation

Follow these steps exactly to get the bot running on your local machine.

### Step 1: Get the Code

First, you need to get the project files onto your computer.

```bash
# Clone the repository from your private GitHub repo
git clone [YOUR_PRIVATE_GITHUB_REPO_LINK_HERE]

# Navigate into the project directory
cd my_binance_bot
```

### Step 2: Set Up Your API Keys (The Most Important Step)

To interact with Binance, you need API keys. We will use the **Binance Testnet** to test the bot safely without risking real money.

1. **Go to the Testnet Website**: Navigate to [https://testnet.binancefuture.com/](https://testnet.binancefuture.com/)

2. **Create a Testnet Account**: You must create a new, separate account here. Your real Binance.com login will not work.

3. **Find "API Management"**: After logging in, hover over your profile icon (top right) and click on **"API Management"**.

4. **Create a New Key**: Give your key a label (e.g., "Python Bot") and click **"Create API"**.

5. **Copy Your Keys**: Binance will show you an **API Key** and an **API Secret**. Copy the API Secret immediately—it will be hidden after you leave this page.

6. **Paste Keys into `.env` File**: In your project folder, open the file named `.env` (create it if it doesn't exist). Paste your keys inside like this:

```env
API_KEY=YOUR_API_KEY_FROM_TESTNET
API_SECRET=YOUR_API_SECRET_FROM_TESTNET
```

> ⚠️ **Important**: The bot's client (`src/client.py`) is already configured to use the Testnet URL, so it will connect to the test environment automatically.

### Step 3: Install Required Python Libraries

This project depends on a few Python libraries.

#### (Optional but Recommended) Create a Virtual Environment

This isolates your project's dependencies from your main system.

```bash
# Create a virtual environment named 'venv'
python -m venv venv

# Activate it (on Windows)
.\venv\Scripts\activate

# Activate it (on macOS/Linux)
source venv/bin/activate
```

#### Install Libraries

Run this command to install all the libraries listed in `requirements.txt`:

```bash
# Install all required libraries
pip install -r requirements.txt
```

✅ **You are now fully set up and ready to run the bot!**

---

## 💻 How to Use the Bot (Usage Examples)

All commands must be run from the root project folder (`my_binance_bot`). The required format is exactly as specified in the assignment.

### Core Orders (Mandatory)

#### 1. Market Order

Places an order that executes immediately at the best available market price.

**Command:**
```bash
python src/market_orders.py [SYMBOL] [SIDE] [QUANTITY]
```

**Example** (Buy 0.001 BTC):
```bash
python src/market_orders.py BTCUSDT BUY 0.001
```

#### 2. Limit Order

Places an order that only executes if the market reaches your specified price or better.

**Command:**
```bash
python src/limit_orders.py [SYMBOL] [SIDE] [QUANTITY] [PRICE]
```

**Example** (Buy 0.001 BTC if the price drops to $50,000):
```bash
python src/limit_orders.py BTCUSDT BUY 0.001 50000
```

---

### Advanced Orders (Bonus)

#### 3. Stop-Limit Order

Places a limit order that is only triggered when the market hits a specific "stop price".

**Command:**
```bash
python src/advanced/stop_limit.py [SYMBOL] [SIDE] [QUANTITY] [STOP_PRICE] [LIMIT_PRICE]
```

**Example** (Place a Stop-Loss for a LONG position):  
This command says: If you are holding 0.001 BTC and the price drops to $59,000 (the `stop_price`), then place a limit order to sell it at $58,950 (the `price`).

```bash
python src/advanced/stop_limit.py BTCUSDT SELL 0.001 59000 58950
```

#### 4. OCO (One-Cancels-the-Other)

This places two orders (a Take-Profit and a Stop-Loss) for an existing position. If one order executes, the other is automatically cancelled. This script places two `reduceOnly` orders to achieve this.

**Command:**
```bash
python src/advanced/oco.py [SYMBOL] [SIDE] [QUANTITY] [TAKE_PROFIT_PRICE] [STOP_LOSS_PRICE]
```

**Example** (Protect an existing 0.001 BTC LONG position):  
This places a limit order to sell at $65,000 (Take Profit) AND a stop order to sell at $59,000 (Stop Loss).

```bash
python src/advanced/oco.py BTCUSDT SELL 0.001 65000 59000
```

#### 5. TWAP (Time-Weighted Average Price)

Executes a large order by splitting it into smaller chunks and placing them at regular intervals over a set period.

**Command:**
```bash
python src/advanced/twap.py [SYMBOL] [SIDE] [TOTAL_QUANTITY] [DURATION_MINUTES]
```

**Example** (Buy 0.1 BTC over the next 30 minutes):  
This script will automatically place 10 smaller market orders of 0.01 BTC, with one order every 3 minutes, to average out the purchase price.

```bash
python src/advanced/twap.py BTCUSDT BUY 0.1 30
```

---

## 📊 Logging and Reporting

### Check Logs

All actions, successful orders, and errors are saved with timestamps in **`bot.log`**. You can check this file to see what the bot has done.

```bash
# View the last 20 lines of the log file
tail -n 20 bot.log

# Or open it in a text editor
cat bot.log
```

### Create Your Report

For your **`report.pdf`**, take screenshots of:
- Your terminal running these commands
- The resulting output in the `bot.log` file
- The Binance Testnet website showing your open orders or trade history

---

## 🔧 Troubleshooting

### Common Issues

1. **"API-key format invalid"**: Double-check your `.env` file. Make sure there are no extra spaces or quotes around your API keys.

2. **"Signature for this request is not valid"**: Your API Secret might be incorrect. Generate a new API key pair from the Testnet.

3. **"Module not found"**: Make sure you've run `pip install -r requirements.txt` and are in the correct directory.

4. **Connection errors**: Verify you're using the Testnet URL in `src/client.py` and that you have an active internet connection.

---

## 📝 Requirements

- Python 3.7 or higher
- Internet connection
- Binance Testnet account

---

## ⚠️ Security Notes

- **Never commit your `.env` file** to GitHub. The `.gitignore` file is configured to prevent this.
- **Use only the Testnet** for development and testing.
- **Keep your API keys private**. Anyone with your keys can trade on your behalf.

---

## 📄 License

This project is created for educational purposes as part of a Python Developer assignment.

---

## 🤝 Support

If you encounter any issues or have questions, please refer to the official [Binance API Documentation](https://binance-docs.github.io/apidocs/futures/en/) or check your `bot.log` file for detailed e