"""
Trading operations for Futu OpenAPI.
Provides methods for placing orders, checking positions, and managing trades.
"""

from futu import TrdSide, OrderType, TrdEnv
from scripts.futu_client import FutuClient
from config.settings import TRADING_ACCOUNT_ID


class TradingManager:
    """
    Manager class for trading operations.
    """

    def __init__(self, client: FutuClient, market="HK", acc_id=None):
        """
        Initialize trading manager.

        Args:
            client: FutuClient instance
            market: Market type ("HK", "US", "SH", "SZ")
            acc_id: Trading account ID (defaults to TRADING_ACCOUNT_ID from settings)
        """
        self.client = client
        self.market = market
        self.acc_id = acc_id or TRADING_ACCOUNT_ID
        self._trade_ctx = None

    def _get_trade_ctx(self):
        """Get trade context, initializing if needed."""
        if self._trade_ctx is None:
            self._trade_ctx = self.client.get_trade_ctx(self.market)
        return self._trade_ctx

    def place_order(self, code, price, quantity, side, order_type=OrderType.NORMAL):
        """
        Place a buy or sell order.

        Args:
            code: Stock code (e.g., "HK.00700", "US.AAPL")
            price: Order price (0 for market orders)
            quantity: Number of shares
            side: TrdSide.BUY or TrdSide.SELL
            order_type: OrderType.NORMAL (limit) or OrderType.MARKET

        Returns:
            dict: Order result with order_id
        """
        ctx = self._get_trade_ctx()

        kwargs = {
            "price": price,
            "qty": quantity,
            "code": code,
            "trd_side": side,
            "order_type": order_type
        }
        if self.acc_id:
            kwargs["acc_id"] = self.acc_id

        ret, data = ctx.place_order(**kwargs)

        if ret != 0:
            raise Exception(f"Failed to place order: {data}")

        return {
            "order_id": data.iloc[0]["order_id"] if len(data) > 0 else None,
            "status": "placed",
            "data": data.to_dict("records") if not data.empty else []
        }

    def get_positions(self, code=None):
        """
        Get current positions.

        Args:
            code: Optional stock code to filter

        Returns:
            list: List of position dictionaries
        """
        ctx = self._get_trade_ctx()

        kwargs = {"code": code}
        if self.acc_id:
            kwargs["acc_id"] = self.acc_id

        ret, data = ctx.position_list_query(**kwargs)

        if ret != 0:
            raise Exception(f"Failed to get positions: {data}")

        return data.to_dict("records") if not data.empty else []

    def get_position(self, code):
        """
        Get position for a specific stock.

        Args:
            code: Stock code

        Returns:
            dict: Position info or None if not found
        """
        positions = self.get_positions(code=code)
        return positions[0] if positions else None

    def get_today_orders(self, status=None):
        """
        Get today's orders.

        Args:
            status: Optional order status filter

        Returns:
            list: List of order dictionaries
        """
        ctx = self._get_trade_ctx()

        kwargs = {"status_filter_list": status}
        if self.acc_id:
            kwargs["acc_id"] = self.acc_id

        ret, data = ctx.order_list_query(**kwargs)

        if ret != 0:
            raise Exception(f"Failed to get orders: {data}")

        return data.to_dict("records") if not data.empty else []

    def get_filled_orders(self):
        """
        Get filled orders.

        Returns:
            list: List of filled order dictionaries
        """
        from futu import OrderStatus
        return self.get_today_orders(status=[OrderStatus.FILLED_ALL, OrderStatus.FILLED_PART])

    def get_pending_orders(self):
        """
        Get pending (unfilled) orders.

        Returns:
            list: List of pending order dictionaries
        """
        from futu import OrderStatus
        return self.get_today_orders(status=[OrderStatus.SUBMITTED, OrderStatus.WAITING_SUBMIT])

    def cancel_order(self, order_id):
        """
        Cancel a pending order.

        Args:
            order_id: Order ID to cancel

        Returns:
            dict: Cancel result
        """
        ctx = self._get_trade_ctx()

        kwargs = {
            "modify_order_op": 0,  # Cancel operation
            "order_id": order_id
        }
        if self.acc_id:
            kwargs["acc_id"] = self.acc_id

        ret, data = ctx.modify_order(**kwargs)

        if ret != 0:
            raise Exception(f"Failed to cancel order: {data}")

        return {
            "order_id": order_id,
            "status": "cancelled",
            "data": data.to_dict("records") if not data.empty else []
        }

    def cancel_all_orders(self):
        """
        Cancel all pending orders.

        Returns:
            list: List of cancel results
        """
        pending = self.get_pending_orders()
        results = []

        for order in pending:
            try:
                result = self.cancel_order(order["order_id"])
                results.append(result)
            except Exception as e:
                results.append({
                    "order_id": order.get("order_id"),
                    "status": "error",
                    "error": str(e)
                })

        return results

    def get_account_info(self):
        """
        Get account information including cash and assets.

        Returns:
            dict: Account information
        """
        ctx = self._get_trade_ctx()

        kwargs = {}
        if self.acc_id:
            kwargs["acc_id"] = self.acc_id

        ret, data = ctx.accinfo_query(**kwargs)

        if ret != 0:
            raise Exception(f"Failed to get account info: {data}")

        if data.empty:
            return {}

        return data.to_dict("records")[0]

    def get_max_trd_qtys(self, code, price):
        """
        Get maximum tradable quantity for a stock.

        Args:
            code: Stock code
            price: Order price

        Returns:
            dict: Maximum quantities for buy/sell
        """
        ctx = self._get_trade_ctx()

        kwargs = {"code": code, "price": price}
        if self.acc_id:
            kwargs["acc_id"] = self.acc_id

        ret, data = ctx.get_max_trd_qtys(**kwargs)

        if ret != 0:
            raise Exception(f"Failed to get max trade qtys: {data}")

        return data.to_dict("records")[0] if not data.empty else {}
