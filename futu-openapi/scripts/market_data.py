"""
Market data operations for Futu OpenAPI.
Provides methods for retrieving quotes, K-lines, and other market data.
"""

from futu import KLType, SubType
from scripts.futu_client import FutuClient


class MarketData:
    """
    Manager class for market data operations.
    """

    def __init__(self, client: FutuClient):
        """
        Initialize market data manager.

        Args:
            client: FutuClient instance
        """
        self.client = client
        self._quote_ctx = None

    def _get_quote_ctx(self):
        """Get quote context, initializing if needed."""
        if self._quote_ctx is None:
            self._quote_ctx = self.client.get_quote_ctx()
        return self._quote_ctx

    def subscribe(self, codes, sub_types=None):
        """
        Subscribe to market data for given stock codes.

        Args:
            codes: Stock code or list of codes (e.g., "HK.00700" or ["HK.00700", "US.AAPL"])
            sub_types: Subscription types, defaults to [QUOTE]

        Returns:
            dict: Subscription result
        """
        ctx = self._get_quote_ctx()

        if isinstance(codes, str):
            codes = [codes]

        if sub_types is None:
            sub_types = [SubType.QUOTE]

        ret, data = ctx.subscribe(codes, sub_types)

        if ret != 0:
            raise Exception(f"Failed to subscribe: {data}")

        return {"status": "subscribed", "codes": codes}

    def unsubscribe(self, codes, sub_types=None):
        """
        Unsubscribe from market data.

        Args:
            codes: Stock code or list of codes
            sub_types: Subscription types to unsubscribe

        Returns:
            dict: Unsubscription result
        """
        ctx = self._get_quote_ctx()

        if isinstance(codes, str):
            codes = [codes]

        if sub_types is None:
            sub_types = [SubType.QUOTE]

        ret, data = ctx.unsubscribe(codes, sub_types)

        if ret != 0:
            raise Exception(f"Failed to unsubscribe: {data}")

        return {"status": "unsubscribed", "codes": codes}

    def get_quote(self, codes):
        """
        Get real-time quote for stocks.

        Args:
            codes: Stock code or list of codes

        Returns:
            list: List of quote dictionaries
        """
        ctx = self._get_quote_ctx()

        if isinstance(codes, str):
            codes = [codes]

        ret, data = ctx.get_stock_quote(codes)

        if ret != 0:
            raise Exception(f"Failed to get quote: {data}")

        return data.to_dict("records") if not data.empty else []

    def get_klines(self, code, period="DAY", count=100, start=None, end=None):
        """
        Get K-line (candlestick) data.

        Args:
            code: Stock code (e.g., "HK.00700")
            period: K-line period ("MIN_1", "MIN_5", "MIN_15", "MIN_30", "MIN_60", "DAY", "WEEK", "MONTH", "YEAR")
            count: Number of K-lines to retrieve
            start: Start date (format: "YYYY-MM-DD")
            end: End date (format: "YYYY-MM-DD")

        Returns:
            list: List of K-line dictionaries
        """
        ctx = self._get_quote_ctx()

        # Map period string to KLType
        period_map = {
            "MIN_1": KLType.K_1M,
            "MIN_5": KLType.K_5M,
            "MIN_15": KLType.K_15M,
            "MIN_30": KLType.K_30M,
            "MIN_60": KLType.K_60M,
            "DAY": KLType.K_DAY,
            "WEEK": KLType.K_WEEK,
            "MONTH": KLType.K_MON,
            "YEAR": KLType.K_YEAR
        }

        kl_type = period_map.get(period, KLType.K_DAY)

        ret, data, page_req_key = ctx.request_history_kl(
            code=code,
            ktype=kl_type,
            autype=None,  # Use default adjustment type
            start=start,
            end=end,
            max_count=count
        )

        if ret != 0:
            raise Exception(f"Failed to get K-lines: {data}")

        return data.to_dict("records") if not data.empty else []

    def get_cur_klines(self, codes, period="DAY", num=100):
        """
        Get current K-line data (real-time).

        Args:
            codes: Stock code or list of codes
            period: K-line period
            num: Number of K-lines

        Returns:
            list: List of K-line dictionaries
        """
        ctx = self._get_quote_ctx()

        if isinstance(codes, str):
            codes = [codes]

        period_map = {
            "MIN_1": KLType.K_1M,
            "MIN_5": KLType.K_5M,
            "MIN_15": KLType.K_15M,
            "MIN_30": KLType.K_30M,
            "MIN_60": KLType.K_60M,
            "DAY": KLType.K_DAY,
            "WEEK": KLType.K_WEEK,
            "MONTH": KLType.K_MON,
            "YEAR": KLType.K_YEAR
        }

        kl_type = period_map.get(period, KLType.K_DAY)

        ret, data = ctx.get_cur_kline(codes, num, kl_type)

        if ret != 0:
            raise Exception(f"Failed to get current K-lines: {data}")

        return data.to_dict("records") if not data.empty else []

    def get_subscription(self):
        """
        Get current subscription list.

        Returns:
            list: List of subscribed stocks
        """
        ctx = self._get_quote_ctx()

        ret, data = ctx.query_subscription()

        if ret != 0:
            raise Exception(f"Failed to get subscription: {data}")

        return data.to_dict("records") if not data.empty else []

    def get_market_snapshot(self, codes):
        """
        Get market snapshot including detailed information.

        Args:
            codes: Stock code or list of codes

        Returns:
            list: List of snapshot dictionaries
        """
        ctx = self._get_quote_ctx()

        if isinstance(codes, str):
            codes = [codes]

        ret, data = ctx.get_market_snapshot(codes)

        if ret != 0:
            raise Exception(f"Failed to get market snapshot: {data}")

        return data.to_dict("records") if not data.empty else []

    def get_stock_basicinfo(self, market, stock_type="STOCK"):
        """
        Get basic information for stocks in a market.

        Args:
            market: Market code ("HK", "US", "SH", "SZ")
            stock_type: Stock type ("STOCK", "IDX", "ETF", etc.)

        Returns:
            list: List of stock basic info dictionaries
        """
        ctx = self._get_quote_ctx()

        ret, data = ctx.get_stock_basicinfo(market, stock_type)

        if ret != 0:
            raise Exception(f"Failed to get stock basic info: {data}")

        return data.to_dict("records") if not data.empty else []
