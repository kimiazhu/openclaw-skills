"""
Core Futu API client for connecting to FutuOpenD.
"""

from futu import OpenQuoteContext, OpenSecTradeContext, TrdEnv
from config.settings import (
    FUTU_HOST,
    FUTU_PORT,
    TRADING_ENV,
    UNLOCK_PASSWORD
)


class FutuClient:
    """
    Wrapper class for Futu API connections.
    Manages both quote and trade contexts.
    """

    def __init__(self, host=None, port=None, trading_env=None):
        """
        Initialize Futu client.

        Args:
            host: FutuOpenD host address (default: 127.0.0.1)
            port: FutuOpenD port (default: 11111)
            trading_env: Trading environment, 'SIMULATE' or 'REAL'
        """
        self.host = host or FUTU_HOST
        self.port = port or FUTU_PORT
        self.trading_env = trading_env or TRADING_ENV

        self._quote_ctx = None
        self._trade_ctx = None

    def get_quote_ctx(self):
        """
        Get or create quote context for market data.

        Returns:
            OpenQuoteContext instance
        """
        if self._quote_ctx is None:
            self._quote_ctx = OpenQuoteContext(
                host=self.host,
                port=self.port
            )
        return self._quote_ctx

    def get_trade_ctx(self, market="HK"):
        """
        Get or create trade context for placing orders.

        Args:
            market: Market type ("HK", "US", "SH", "SZ")

        Returns:
            OpenSecTradeContext instance
        """
        if self._trade_ctx is None:
            trd_env = TrdEnv.SIMULATE if self.trading_env == "SIMULATE" else TrdEnv.REAL

            self._trade_ctx = OpenSecTradeContext(
                host=self.host,
                port=self.port,
                filter_trdmarket=market,
                trd_env=trd_env
            )

            # Unlock trading if password is set
            if UNLOCK_PASSWORD and self.trading_env == "REAL":
                ret, data = self._trade_ctx.unlock_trade(UNLOCK_PASSWORD)
                if ret != 0:
                    raise Exception(f"Failed to unlock trading: {data}")

        return self._trade_ctx

    def close(self):
        """Close all connections."""
        if self._quote_ctx:
            self._quote_ctx.close()
            self._quote_ctx = None
        if self._trade_ctx:
            self._trade_ctx.close()
            self._trade_ctx = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
