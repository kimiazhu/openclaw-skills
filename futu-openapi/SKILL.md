---
name: futu-openapi
description: This skill enables automated stock trading through Futu Open API. It provides capabilities to buy/sell stocks, query positions, check order status, and retrieve market data. This skill should be used when users need to programmatically trade Hong Kong stocks, US stocks, or A-shares through Futu securities.
---

# Futu OpenAPI Trading

## Overview

This skill provides programmatic access to Futu OpenAPI for automated stock trading. It supports:
- Placing buy/sell orders (market and limit orders)
- Querying account positions and balances
- Checking order status and history
- Retrieving real-time market data and K-line data
- Cancelling pending orders

## Prerequisites

Before using this skill, ensure you have:
1. A Futu securities account with OpenAPI access enabled
2. FutuOpenD software installed and running
3. Python 3.7+ with `futu-api` package installed (`pip install futu-api`)
4. API connection configuration (host, port, unlock password if needed)

## File Structure

```
futu-openapi/
├── SKILL.md                  # This documentation
├── scripts/
│   ├── futu_client.py       # Core Futu API client
│   ├── trading.py           # Trading operations
│   └── market_data.py       # Market data retrieval
└── config/
    └── settings.py          # Configuration settings
```

## Core Capabilities

### 1. Connect to Futu API
ls

Establish connection to FutuOpenD:

```python
from scripts.futu_client import FutuClient

# Initialize client
client = FutuClient(host="127.0.0.1", port=11111)

# Connect to trading server
trader = client.get_trade_ctx()
```

### 2. Place Orders

Buy or sell stocks:

```python
from scripts.trading import TradingManager
from futu import TrdSide, OrderType

# Initialize trading manager
trading = TradingManager(client)

# Place a limit buy order
result = trading.place_order(
    code="HK.00700",           # Stock code
    price=380.0,               # Order price
    quantity=100,              # Quantity (lot size)
    side=TrdSide.BUY,          # BUY or SELL
    order_type=OrderType.NORMAL  # NORMAL (limit) or MARKET
)

# Place market order
result = trading.place_order(
    code="US.AAPL",
    price=0,                   # 0 for market order
    quantity=10,
    side=TrdSide.SELL,
    order_type=OrderType.MARKET
)
```

### 3. Query Positions

Get current holdings:

```python
from scripts.trading import TradingManager

# Get all positions
positions = trading.get_positions()

# Get specific stock position
position = trading.get_position(code="HK.00700")
```

### 4. Check Orders

Query order status and history:

```python
# Get today's orders
orders = trading.get_today_orders()

# Get filled orders
filled_orders = trading.get_filled_orders()

# Get pending orders
pending_orders = trading.get_pending_orders()
```

### 5. Cancel Orders

Cancel pending orders:

```python
# Cancel specific order
result = trading.cancel_order(order_id="123456789")

# Cancel all pending orders
result = trading.cancel_all_orders()
```

### 6. Get Market Data

Retrieve real-time quotes and historical data:

```python
from scripts.market_data import MarketData

# Initialize market data client
market = MarketData(client)

# Get real-time quote
quote = market.get_quote("HK.00700")

# Get K-line data (daily candles)
klines = market.get_klines(
    code="HK.00700",
    period="DAY",           # DAY, WEEK, MONTH, YEAR, MIN_1, MIN_5, etc.
    count=100               # Number of candles
)

# Get subscription list
sub_list = market.get_subscription()
```

## Market Type Reference

| Market | Code Prefix | Example |
|--------|-------------|---------|
| Hong Kong | HK. | HK.00700 (Tencent) |
| US Stocks | US. | US.AAPL (Apple) |
| Shanghai | SH. | SH.600519 (Kweichow Moutai) |
| Shenzhen | SZ. | SZ.000001 (Ping An Bank) |

## Order Type Reference

```python
from futu import TrdSide, OrderType

# Order Sides
TrdSide.BUY      # Buy order
TrdSide.SELL     # Sell order

# Order Types
OrderType.NORMAL # Limit order
OrderType.MARKET # Market order
```

## Configuration

Edit `config/settings.py` to customize:

```python
# FutuOpenD connection settings
FUTU_HOST = "127.0.0.1"
FUTU_PORT = 11111

# Trading environment
TRADING_ENV = "SIMULATE"  # SIMULATE or REAL

# Default market
DEFAULT_MARKET = "HK"

# Trading Account ID (optional but recommended for multi-account setups)
# All trading operations will be executed in this specific account
TRADING_ACCOUNT_ID = "1001219209771234"  # Replace with your account ID
```

### Multi-Account Support

If you have multiple Futu accounts, you can:

1. **Set default account in settings.py:**
   ```python
   TRADING_ACCOUNT_ID = "1001219209771234"
   ```

2. **Override per TradingManager instance:**
   ```python
   # Use specific account for this manager
   trading = TradingManager(client, market="HK", acc_id="1001219209771234")
   ```

When `TRADING_ACCOUNT_ID` is set, all operations (place_order, get_positions, get_today_orders, etc.) will automatically use this account.

## Usage Examples

### Example 1: Buy Tencent Stock

```python
from scripts.futu_client import FutuClient
from scripts.trading import TradingManager
from futu import TrdSide, OrderType

# Initialize
client = FutuClient()
trading = TradingManager(client)

# Place buy order for Tencent
result = trading.place_order(
    code="HK.00700",
    price=380.0,
    quantity=100,
    side=TrdSide.BUY,
    order_type=OrderType.NORMAL
)
print(f"Order placed: {result}")
```

### Example 2: Monitor Portfolio

```python
# Get all positions
positions = trading.get_positions()
for pos in positions:
    print(f"{pos['code']}: {pos['qty']} @ {pos['cost_price']}")

# Get account info
account = trading.get_account_info()
print(f"Cash: {account['cash']}, Total Assets: {account['total_assets']}")
```

### Example 3: Get Real-time Quotes

```python
from scripts.market_data import MarketData

market = MarketData(client)

# Subscribe to multiple stocks
market.subscribe(["HK.00700", "US.AAPL", "HK.03690"])

# Get quotes
quotes = market.get_quote(["HK.00700", "US.AAPL"])
for quote in quotes:
    print(f"{quote['code']}: {quote['last_price']}")
```

## Error Handling

All operations may raise exceptions. Always wrap calls in try-except:

```python
from futu import FTAPIError

try:
    result = trading.place_order(...)
except FTAPIError as e:
    print(f"API Error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Notes

- Always test with `SIMULATE` environment before real trading
- Check stock lot sizes (e.g., HK stocks typically have 100, 500, or 1000 share lots)
- Market orders may have slippage, especially in volatile markets
- Ensure sufficient funds before placing orders
- Be aware of trading hours for different markets

## References

- [Futu OpenAPI Documentation](https://openapi.futunn.com/)
- [Futu API Python SDK](https://github.com/FutunnOpen/futu-api)
