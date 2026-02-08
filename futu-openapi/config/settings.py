"""
Configuration settings for Futu OpenAPI trading.
"""

# FutuOpenD connection settings
FUTU_HOST = "127.0.0.1"
FUTU_PORT = 11111

# Trading environment
# Options: "SIMULATE" or "REAL"
TRADING_ENV = "SIMULATE"

# Default market
# Options: "HK" (Hong Kong), "US" (US Stocks), "SH" (Shanghai), "SZ" (Shenzhen)
DEFAULT_MARKET = "HK"

# Unlock password (if required for trading)
UNLOCK_PASSWORD = None

# API Rate Limiting
MAX_REQUESTS_PER_SECOND = 10

# Default order settings
DEFAULT_ORDER_TIMEOUT = 30  # seconds

# Trading Account ID
# Specify the Futu account ID to use for all trading operations
# Example: "1001219209771234"
TRADING_ACCOUNT_ID = None
